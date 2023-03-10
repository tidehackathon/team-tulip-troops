import unicodedata
import transformers
import json
import re

tokenizer = transformers.AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
model = transformers.AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
nlp = transformers.pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def get_entities(input):
    global tokenizer, model, nlp
    input_dict = input
    if 'cleanRenderedContent' not in input_dict:
        input_dict = clean_data(input_dict)
    entities = []
    for e in nlp(input_dict['cleanRenderedContent']):
        entities.append({
            'entity_group': str(e['entity_group']),
            'score': float(e['score'].item()),
            'word': str(e['word']),
            'start': int(e['start']),
            'end': int(e['end']),
        })
    input_dict['entities'] = entities
    print(entities)
    return entities
    # return json.loads(json.dumps(input_dict))


def clean_data(input_dict):
    text = input_dict['renderedContent']
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = text.replace('\n', ' ').lower()

    # Remove urls, hashtags and user mentions
    text = re.sub(r'\#', ' ', f' {text} ')
    text = re.sub(r'\s\@\S+', ' ', f' {text} ')
    text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', text)
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip().title()

def display_entities(input_jsonstr):
    input_dict = json.loads(input_jsonstr)
    if 'entities' not in input_dict:
        input_dict = json.loads(get_entities(input_jsonstr))

    text = input_dict['renderedContent']
    for enitiy in reversed(input_dict['entities']):
        badgef = '<span class="badge text-bg-secondary"><i class="bx bxs-invader"></i> {:s}</span>'
        if enitiy['entity_group'] == 'PER':
            badgef = '<span class="badge text-bg-danger"><i class="bx bxs-user"></i> {:s}</span>'
        if enitiy['entity_group'] == 'ORG':
            badgef = '<span class="badge text-bg-warning"><i class="bx bxs-bank"></i> {:s}</span>'
        elif enitiy['entity_group'] == 'LOC':
            badgef = '<span class="badge text-bg-primary"><i class="bx bxs-map"></i> {:s}</span>'
        
        text = text[:enitiy['start']].rstrip() +" "+ badgef.format(enitiy['word'].strip()) +" "+ text[enitiy['end']+1:].lstrip()
        #text = text.replace(enitiy['word'].strip(), )
    return f'<div class="card"><div class="card-body">{text:s}</div></div>'

if __name__ == '__main__':
    import pandas as pd
    df = pd.read_csv("../../../data/Ukraine_border.csv",engine="python",on_bad_lines='skip')
    
    with open("index.html","w") as fh:
        fh.write('<!doctype html>')
        fh.write('<html lang="en"><head><meta charset="utf-8">')
        fh.write('<meta name="viewport" content="width=device-width, initial-scale=1"><title>Bootstrap demo</title>')
        fh.write('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">')
        fh.write('<link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">')
        fh.write('</head><body><div class="container"><h1>Tweets</h1>')
        
        for tweetid, tweet in df.head(25).iterrows():
            tweetjson = json.dumps(tweet.to_dict())
            tweetjson = get_entities(tweetjson)
            tweethtml = display_entities(tweetjson)
            
            fh.write(tweethtml)
        fh.write('</div><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>')
        fh.write('</body></html>')
