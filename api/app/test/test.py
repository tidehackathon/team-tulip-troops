import requests

api_key = 'AIzaSyDQIiI_WMFep30s0Xbz6bcSyog29Qb2mpw'
headers = {'Accept': 'application/json'}
query_parameters = {
    "key": api_key,
    "query": 'ChatGPT lists Trump, Elon Musk as controversial and worthy of special treatment, Biden and Bezos as not.  I\'ve got more examples. '
}




x = requests.get('https://factchecktools.googleapis.com/v1alpha1/claims:search', headers=headers, params=query_parameters)

print(x.status_code)
print(x.json)