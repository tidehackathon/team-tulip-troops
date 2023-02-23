# How to get this repo running
0. Clone this repo
```
$ git clone git@github.com:tidehackathon/team-tulip-troops.git
```
1. Fetch the Google Search API-keys (see below)
2. Start a ElasticSearch and Kibana Instance (see below)
3. Create a virtual environment:
```
$ python3 -m venv venv
```
4. Activate the virtual environment:
```
$ pip install -r requirements.txt
```
5. Run FastAPI server for development
```
$ uvicorn app.main:app --host localhost --port 8000 --reload
```
6. Install nodejs version 14 or higher
7. Install the Angular CLI version 15 or higher:
```
$ npm install -g @angular/cli
```
8. Navigate to the `frontend` folder
9. Install the Node modules
```
$ npm install
```
10. Serve the frontend
```
$ ng serve
```
11. Go to http://localhost:4200

## How to get the Google API-keys
([Source](https://mixedanalytics.com/knowledge-base/import-google-serp-data-to-google-sheets/))

1. While logged into your Google account, navigate to https://programmablesearchengine.google.com/controlpanel/all, and click Add
2. You'll be prompted to configure your custom search engine. Give your Search Engine a name, and choose to search the entire web (unless you specifically want to limit your results to a subset of pages). Click Create.
3. Your search engine has been created. Click Customize.
4. Scroll down the page and optionally adjust any settings. Note the search engine ID as we'll need that soon.
5. Navigate to the Custom Search JSON API page at https://developers.google.com/custom-search/v1/overview#api_key and click Get a Key.
6. Choose an existing project, or create a new one, and click Next.
7. Note and copy your API key, you'll need this along with your custom search engine ID.
8. Create a file called `.env` in the `pipeline/src`-folder.
9. Add the keys to this file as follows:
```
GOOGLE_API_KEY=<YOUR_API_KEY>
GOOGLE_CSE_ID=<YOUR_SEARCH_ENGINE_ID>
```

## How to start with ElasticSearch/Kibana?
1. Start the Free Trial (14 days) on https://www.elastic.co/
2. Login
3. Go to Integrations -> Python
4. Right corner click "View deployment details"
5. Copy Cloud ID and Create API key (replace those in .env)
7. Go to Stack Management -> Saved Objects -> Import "kibana_export_dashboard.ndjson" 
8. Start the FAST API and Angular Frontend
