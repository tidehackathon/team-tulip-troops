from sentence_transformers import CrossEncoder
from transformers import pipeline
import requests
import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize
import torch
import re
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings() 

import get_evidences
import summarization

if torch.cuda.is_available():    
    device = torch.device("cuda:0")
    print('GPU used for claim checker: {}'.format(torch.cuda.get_device_name(0)))
else:
    device = torch.device("cpu")

nli_model = CrossEncoder('MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli', device=device)
zero_shot_model = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli", device=device)

def investigate_claim(claim, model_type='zero-shot', filter_opinions=True):
    
    # Determine if claim or opinion
    res, score = claim_or_opinion(claim)
    if  res == 'claim' or not filter_opinions:
        # summarize claim if needed
        if len(claim.split(' ')) > 50:
            print('Summarizing claim for further processing.')
            claim = summarization.summarize_text(claim, max_len=50)

        evidence = collect_evidence(claim, num_results=10)
            
        conclusions = []
        confidences = []
        # TODO vectorize this
        for i, row in evidence.iterrows():
            source, text, summary = row.source, row.text, row.summary

            if len(summary) == 0:
                print('Warning: no summary found for evidence.')
                text_input = text
            elif len(text) < 3000:
                text_input = text
            else:
                text_input = summary
            
            if model_type == 'zero-shot':
                label, confidence = apply_zero_shot_model(claim, text_input)
            elif model_type == 'nli':
                label, confidence = apply_nli_model(claim, text_input)
            else:
                raise ValueError('No valid model type specified.')
                
            conclusions += [label]
            confidences += [confidence]

        evidence['conclusion'] = conclusions

        # get clean source name
        cleaned_sources = ['.'.join(urlparse(s).netloc.split('.')[-2:-1]) for s in evidence.source.values]
        evidence['cleaned_source'] = cleaned_sources

        # determine source credibility
        sources_cred = [cred[1] * -1 if 'uncredible' in cred[0] else cred[1] for cred in check_source_credibility(cleaned_sources)]
        evidence['source_trust'] = sources_cred

        # Remove sources that are too unreliable
        unreliable_evidence = evidence[evidence['source_trust'] < -0.6]
        evidence = evidence[evidence['source_trust'] > -0.6]

        # filter evidence 
        parse_conclusions(evidence['conclusion'].values, 
                          evidence['source_trust'].values)

        # Re-add unreliable evidence for analysis
        evidence = pd.concat([evidence, unreliable_evidence])
        evidence['used_as_evidence'] = evidence['source_trust'] > -0.6
        
        return evidence
    else:
        print(f'This is not a claim (confidence: {round(score,2)}). Not checking for factual correctness.')
        return None

def collect_evidence(claim, num_results):
    try:
        evidence = load_evidence(claim)
        print('Existing evidence results found locally, loading from disk.')
    except:
        links = get_evidences.get_top_k_results_from_google(claim, k=num_results)
        evidence = [(l, flatten_evidence(get_evidences.get_relevant_text_from_webpage(l))) for l in links]

        # Remove empty evidence
        evidence = pd.DataFrame([ev for ev in evidence if len(ev[1]) > 0], columns=['source', 'text'])
        
        # Clean input
        evidence['text'] = evidence['text'].apply(lambda x: clean_input(x))
    
        # Remove duplicates
        evidence.drop_duplicates('text', inplace=True)

        # Add summarization
        evidence['summary'] = summarization.summarize_text(list(evidence['text'].values))

        # Save for later use
        save_evidence(evidence, claim)
        
    return evidence

def parse_conclusions(conclusions, sources_cred):
    num_sources = len(conclusions)
    
    score_mapping = {'true':1, 'false':-1, 'neutral':-0.1}
    conclusion_scores = [score_mapping[c] for c in conclusions]
    total_score = sum(conclusion_scores)
    
    print(f'Conclusions: {conclusions}')
    
    # rescale score to 0 - 1
    normalized_score = round((10 + total_score) / 20, 2)
    
    print(f'The truth score of this claim is {normalized_score} (scaled between 0 and 1)\n')
    
    return normalized_score

# Models

def claim_or_opinion(text):
    res = zero_shot_model(text, ['claim', 'opinion'])
    return res['labels'][0], res['scores'][0]

def check_nation_affiliation(text, nation):
    res = zero_shot_model(text, [f'{nation} affiliation', f'no {nation} affiliation'])
    return res['labels'][0], res['scores'][0]

def check_source_credibility(source_name):
    res = zero_shot_model(source_name, ['uncredible source', 'credible source'])
    if type(source_name) == str:
        return res['labels'][0], res['scores'][0]
    else:
        return [(r['labels'][0], r['scores'][0]) for r in res]

def apply_zero_shot_model(claim, text):
    global zero_shot_model
    unsure_threshold = 0.4

    zeroshot_labels = [f"The following statement is True: {claim}",
                       f'Not enough information to verify the following statement: {claim}',
                       f"The following statement is False: {claim}"]

    conclusion = zero_shot_model(text, candidate_labels=zeroshot_labels)
    parsed_conclusion = conclusion['labels'][0].split(' ')[4].lower().replace(':', '')
    if parsed_conclusion == 'true':
        result = True
    elif parsed_conclusion == 'false':
        result = False
    else:
        result = 'neutral'
        
    score = conclusion['scores'][0]
    
    return str(result).lower() if score > unsure_threshold else 'neutral', score

def apply_nli_model(claim, text):
    global nli_model
    label_mapping = ['false', 'true', 'neutral']   # (['contradiction', 'entailment', 'neutral'])

    scores = nli_model.predict([(claim, text)])
    
    #Convert score to label
    label = label_mapping[scores.argmax(axis=1)[0]]
    confidence = scores[scores.argmax(axis=1)[0]]

    return label, confidence

# Pre/post-processing functions

def clean_input(text):
    # Remove newline
    text = text.replace('\n', ' ')
    return text

def split_to_sentences(text):
    return sent_tokenize(text, language='english')

def flatten_evidence(parsed_evidence):
    if type(parsed_evidence) == str:
        return parsed_evidence
    else:
        return ' '.join([' '.join([' '.join([el if len(el)>2 else '' for el in sl]).strip() for sl in lst]) for lst in parsed_evidence]).strip()


## File related functions

def save_evidence(evidence, claim):
    claim = re.sub('[\W_]+', '', claim)
    pd.DataFrame(evidence).to_csv(f"../data/temp/{claim}.csv", sep ='\t')
    
def load_evidence(claim):
    claim = re.sub('[\W_]+', '', claim)
    evidence = pd.read_csv(f"../data/temp/{claim}.csv", sep ='\t')
    return evidence