import json
import transformers
import unicodedata


classifier = transformers.pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def clean_data(input_dict):
    tweetcontent = unicodedata.normalize('NFKD', input_dict['renderedContent']).encode('ascii', 'ignore').decode()
    input['cleanRenderedContent'] = tweetcontent.replace("\n\n","").replace("\n",". ")
    return input

def get_sentiment(input_jsonstr):
    global classifier
    input = json.loads(input_jsonstr)
    if 'cleanRenderedContent' not in input:
        input = clean_data(input)
    emotion = classifier(input['cleanRenderedContent'])
    input['emotion'] = {e['label']: e['score'] for e in emotion[0]}
    return json.dumps(input)

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