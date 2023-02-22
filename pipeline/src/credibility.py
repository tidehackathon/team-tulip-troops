import hashlib
import json
import requests
import os
import unicodedata
import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse

import transformers
import sentence_transformers
import nltk.tokenize
import torch

from elasticsearch import Elasticsearch

requests.packages.urllib3.disable_warnings()

from . import get_evidences
from . import summarization

if torch.cuda.is_available():    
    device = torch.device("cuda:0")
    print('GPU used for claim checker: {}'.format(torch.cuda.get_device_name(0)))
else:
    device = torch.device("cpu")

nli_model = None
zero_shot_model = None

# Found in the 'Manage this deployment' page
CLOUD_ID = "3b7c7ef1ec744d898bf05ea60d28d2de:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDVmNWNkY2UyOTFlMjQ3YWE5YjhmMWZlNjgyM2Y2NTE4JDRjOTY5N2YzYmY2ZjQwY2I5MmU4NWNkY2UzNjRlZjU1"

# Found in the 'Management' page under the section 'Security'
API_KEY = "ZjNHMFRJWUJETGVSREluRXdLVnY6VGl1d3NPQjdSRWF5aU1aQVRFSkRnQQ=="

def investigate_tweet(input_jsonstr):
    input_dict = json.loads(input_jsonstr)
    if 'cleanRenderedContent' not in input_dict:
        input_dict = clean_tweet(input_dict)
    result = investigate_claim(input_dict['cleanRenderedContent'])
    input_dict.update(result)
    return json.dumps(input_dict)

def investigate_claim(claim, datasource="google", model_type="nli", num_results=10, filter_opinions=True):
    """Investigates the claim based on evidence collected"""

    # Determine if claim or opinion
    res, score = claim_or_opinion(claim)

    if res == 'claim' or not filter_opinions:
         # summarize claim if needed
        if len(claim.split(' ')) > 50:
            print('Summarizing claim for further processing.')
            claim = summarization.summarize_text(claim, max_len=50)

        evidences = collect_evidences(claim, datasource=datasource, num_results=num_results)
        evidences = evidences.assign(text_input = evidences['text'])
        use_summary = (evidences['summary'].str.len()>0) & (evidences['text'].str.len()>3000)
        evidences.loc[use_summary,'text_input'] = evidences.loc[use_summary,'summary']

        evidences = evidences.loc[evidences.text_input.str.strip()!="",:]

        if model_type == "nli":
            evidences[['label','confidence']] = evidences.apply(run_nli_model,result_type='expand',axis=1, claim=claim)
        elif model_type == "zero-shot":
            evidences[['label','confidence']] = evidences.apply(run_zero_shot_model,result_type='expand',axis=1, claim=claim)
        else:
            raise NotImplementedError()

        # get clean source name
        cleaned_sources = ['.'.join(urlparse(s).netloc.split('.')[-2:-1]) for s in evidences.source.values]
        evidences['cleaned_source'] = cleaned_sources

        # determine source credibility
        sources_cred = [cred[1] * -1 if 'uncredible' in cred[0] else cred[1] for cred in check_source_credibility(cleaned_sources)]
        evidences['source_trust'] = sources_cred

        # Remove sources that are too unreliable
        unreliable_evidence = evidences[evidences['source_trust'] < -0.6]
        evidences = evidences[evidences['source_trust'] > -0.6]

        # Compute trust score
        label_counts = evidences['label'].value_counts().to_dict()
        label_weights = {'false': -1., 'neutral': -0.1, 'true': 1.}
        score = sum([label_counts.get(l,0)*w for l,w in label_weights.items()])
        norm_score = round((10 + score) / 20, 2)

        # Re-add unreliable evidence for analysis
        evidences = pd.concat([evidences, unreliable_evidence])
        evidences['used_as_evidence'] = evidences['source_trust'] > -0.6

        # Build results dict
        evidences_dict = evidences.to_dict("records")
        
        return {
            'credibility_score': norm_score,
            'credibility_evidences': evidences_dict
        }
    else:
        print(f'This is not a claim (confidence: {round(score,2)}). Not checking for factual correctness.')
        return None # TODO wat returnen we voor de API?

def collect_evidences(claim, datasource='google', num_results=10):
    evidences = load_evidences(claim, datasource)
    if evidences is False:
        if datasource=='google':
            evidences = fetch_evidences_google(claim, num_results=num_results)
        elif datasource=='elastic':
            evidences = fetch_evidences_elastic(claim, num_results=num_results)
        else:
            raise NotImplementedError()
        save_evidences(claim, datasource, evidences)
    return evidences

def fetch_evidences_google(claim, num_results=10):
    links = get_evidences.get_top_k_results_from_google(claim, k=num_results)
    evidenceDF = pd.DataFrame(links,columns=['source'])
    evidenceDF = evidenceDF.assign(text = evidenceDF['source'].apply(fetch_evidence_from_link))
    evidenceDF = evidenceDF.drop_duplicates('text')
    evidenceDF = evidenceDF.loc[evidenceDF['text'].str.strip()!=""]
    evidenceDF = evidenceDF.assign(summary = summarization.summarize_text(list(evidenceDF['text'].values)))
    return evidenceDF

def fetch_evidence_from_link(link):
    evidence = get_evidences.get_relevant_text_from_webpage(link)
    evidence = flatten_evidence(evidence)
    evidence = clean_input(evidence)
    return evidence

def fetch_evidences_elastic(claim):
    es = Elasticsearch(
        cloud_id=CLOUD_ID,
        api_key=API_KEY,
    )
    resp = es.search(index="news_articles", query={"query_string": {"query": claim}})
    evidences = []
    for hit in resp['hits']['hits']:
        evidences.append({
            'source': hit["_source"]['news_paper'] + " - " + hit["_source"]['published'] + " - " + hit["_source"]['headlines'],
            'text': hit["_source"]['headlines'] + "\n\n" + hit["_source"]['articles'],
        })
    evidenceDF = pd.DataFrame(evidences)
    evidenceDF = evidenceDF.drop_duplicates('text')
    evidenceDF = evidenceDF.loc[evidenceDF['text'].str.strip()!=""]
    evidenceDF = evidenceDF.assign(summary = summarization.summarize_text(list(evidenceDF['text'].values)))
    return evidenceDF

def load_evidences(claim, datasource):
    claimhash = hash_claim(claim)
    filename = f"../data/temp/{datasource:s}_{claimhash:s}.csv"
    if os.path.isfile(filename):
        evidence = pd.read_csv(filename, sep ='\t')
        return evidence
    return False

def save_evidences(claim, datasource, evidences):
    claimhash = hash_claim(claim)
    filename = f"../data/temp/{datasource:s}_{claimhash:s}.csv"
    evidences.to_csv(filename, sep ='\t')

def hash_claim(claim):
    return hashlib.sha256(claim.encode()).hexdigest()


# Models

def claim_or_opinion(text):
    global zero_shot_model
    if zero_shot_model is None:
        zero_shot_model = initialize_zero_shot()

    res = zero_shot_model(text, ['claim', 'opinion'])
    return res['labels'][0], res['scores'][0]

def check_nation_affiliation(text, nation):
    global zero_shot_model
    if zero_shot_model is None:
        zero_shot_model = initialize_zero_shot()

    res = zero_shot_model(text, [f'{nation} affiliation', f'no {nation} affiliation'])
    return res['labels'][0], res['scores'][0]

def check_source_credibility(source_name):
    global zero_shot_model
    if zero_shot_model is None:
        zero_shot_model = initialize_zero_shot()

    res = zero_shot_model(source_name, ['uncredible source', 'credible source'])
    if type(source_name) == str:
        return res['labels'][0], res['scores'][0]
    else:
        return [(r['labels'][0], r['scores'][0]) for r in res]

def run_zero_shot_model(row, claim, unsure_threshold=0.4):
    global zero_shot_model

    if zero_shot_model is None:
        zero_shot_model = initialize_zero_shot()

    if row.text_input:
        zeroshot_labels = [f"The following statement is True: {claim}",
                        f"Not enough information to verify the following statement: {claim}",
                        f"The following statement is False: {claim}"]
        conclusion = zero_shot_model(row.text_input, candidate_labels=zeroshot_labels)
        parsed_conclusion = conclusion['labels'][0].split(' ')[4].lower().replace(':', '')

        confidence = conclusion['scores'][0]
        label = 'neutral' if confidence <= unsure_threshold else(
            parsed_conclusion if parsed_conclusion in ['true','false'] else 'neutral')
        return [label,confidence]
    else:
        return ['empty',0.0]

def run_nli_model(row, claim, unsure_threshold=0.0):
    global nli_model

    if nli_model is None:
        nli_model = initialize_nli()

    label_mapping = ['false', 'true', 'neutral']   # (['contradiction', 'entailment', 'neutral'])
    scores = nli_model.predict([(claim, row.text_input)])
    
    confidence = scores[scores.argmax(axis=1)[0]]
    label = 'neutral' if confidence <= unsure_threshold else label_mapping[scores.argmax(axis=1)[0]]
    return [label,confidence]

def initialize_zero_shot():
    return transformers.pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli")

def initialize_nli():
    return sentence_transformers.CrossEncoder('MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli')

# Pre/post-processing functions

def clean_tweet(input_dict):
    tweetcontent = unicodedata.normalize('NFKD', input_dict['renderedContent']).encode('ascii', 'ignore').decode()
    input_dict['cleanRenderedContent'] = tweetcontent.replace("\n\n","").replace("\n",". ")
    return input_dict

def clean_input(text):
    # Remove newline
    text = text.replace('\n', ' ')
    return text

def split_to_sentences(text):
    return nltk.tokenize.sent_tokenize(text, language='english')

def flatten_evidence(parsed_evidence):
    if type(parsed_evidence) == str:
        return parsed_evidence
    else:
        return ' '.join([' '.join([' '.join([el if len(el)>2 else '' for el in sl]).strip() for sl in lst]) for lst in parsed_evidence]).strip()
    

if __name__=='__main__':
    import time
    start = time.time()
    print("Starting", start)
    claim = "brad pitt is to marry with britney spears"
    result = investigate_claim(claim, model_type='zero-shot')
    print(json.dumps(result,indent=4))
    print("Finish", time.time())
    print("Duration", time.time()-start)