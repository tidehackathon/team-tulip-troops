# https://programmablesearchengine.google.com/controlpanel/overview?cx=018062583803202450038%3Aaxp8v-eokms
# https://developers.google.com/custom-search/v1/introduction
# https://console.cloud.google.com/ to get and manage API keys

import time
import urllib
import os
from dotenv import load_dotenv

# from googlesearch import search
from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')

google_service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

def get_top_k_results_from_google(text, k):
    res = google_service.cse().list(q=text, cx=GOOGLE_CSE_ID, num=min(10, k), filter=1).execute()
    if 'spelling' in res.keys():
        res = google_service.cse().list(q=res['spelling']['correctedQuery'], cx=GOOGLE_CSE_ID, num=min(10, k), filter=1).execute()
    if 'items' in res.keys():
        res = [r['link'] for r in res['items'] if (
            '.pdf' not in r['link'] and 
            'twitter.com' not in r['link'] and 
            'facebook.com' not in r['link'] and 
            'youtube' not in r['link'] and
            '.txt' not in r['link']
        )]
        return res[:k]
    else:
        return []

# # old function below
# def get_top_k_results_from_google(text, k):
#     text = urllib.parse.quote_plus(text)
#     res = search(text)
#     res = [r for r in res if '.pdf' not in r and 'twitter.com' not in r and 'facebook.com' not in r]
#     if res:
#         return res[:k]
#     else:
#         return []

def get_relevant_text_from_webpage(url_link):
    try:
        request = requests.get(url_link, verify=False, timeout=20)
    except Exception as e:
        print(f'Webscrape warning, failed for url {url_link}: {e}')
        return '', url_link

    # time.sleep(1)
    Soup = BeautifulSoup(request.text, 'lxml')
    if 'hindi news' in Soup.text.lower() or 'hindi samachar' in Soup.text.lower() or '/download' in request.url :
        return [], request.url

    if '.xlsx' in request.url or '.txt' in request.url:
        return [], request.url

    if '.pdf' in request.url.lower():
        return [], request.url

    if '%PDF-' in request.text:
        return [], request.url

    # creating a list of all common heading tags
    heading_tags = ['h{}'.format(h) for h in range(1, 10)] + ['p']
    results = []

    for tags in Soup.find_all(heading_tags):
        if 'h' in tags.name:
            tokens = tags.text.strip().split()
            if len(tokens) > 8:
                results.append([tags.name, tags.text.strip()])
        else:
            tokens = tags.text.strip().split()
            if len(tokens) > 20:
                results.append([tags.name, tags.text.strip()])
    return results, request.url

if __name__ == '__main__':
    # q = 'Politically Correct Woman (Almost) Uses Pandemic as Excuse Not to Reuse Plastic Bag https://t.co/thF8GuNFPe #coronavirus #nashville'
    # links = get_top_k_results_from_google("joe biden classified documents found", k=3)
    links = get_top_k_results_from_google("brad pitt is to marry with britney spears", k=3)
    print(links)
    for l in links:
        print(get_relevant_text_from_webpage(l))

    # url = 'https://twitter.com/TheOnion'
    # data = requests.get(url)
    # print(data.text)
