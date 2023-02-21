# Parquet Reader API based on FastAPI


## Development

Run the api locally using ```uvicorn``` with auto reload enabled.

### Create venv

~~~bash
python3 -m venv venv
~~~

### Install dependencies

~~~bash
pip install -r requirements.txt
~~~

### Run server for development

~~~bash
uvicorn app.main:app --host localhost --port 8000 --reload
~~~

### Build container for production

~~~bash
docker build -t tulip-analyser .
~~~

## Production

Deploy to Google Cloud Run using VSCode extention `Google Cloud Code`
