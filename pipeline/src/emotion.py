import json
import transformers
import unicodedata
import re


classifier = transformers.pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

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

def get_sentiment(input):
    global classifier
    input_dict = input
    if 'cleanRenderedContent' not in input_dict:
        input_dict = clean_data(input_dict)
    emotion = classifier(input_dict['cleanRenderedContent'])
    input_dict['emotion'] = {e['label']: e['score'] for e in emotion[0]}
    return json.loads(json.dumps(input_dict))

################################
# Example implement
################################
#
# import pandas as pd
# import unicodedata
#
# df = pd.read_csv("../../../data/Ukraine_border.csv",engine="python",on_bad_lines='skip')
#
# for tweetid, tweet in df.head(25).iterrows():
#    tweetcontent = unicodedata.normalize('NFKD', tweet['renderedContent']).encode('ascii', 'ignore').decode()
#    tweetcontent = tweetcontent.replace("\n\n","").replace("\n",". ")
#    tweetobj = json.dumps({'content':tweetcontent})
#    print(tweetid, get_sentiment(tweetobj))