import json
import transformers


classifier = transformers.pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

def get_sentiment(input_jsonstr):
    global classifier
    input = json.loads(input_jsonstr)
    emotion = classifier(input['content'])
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