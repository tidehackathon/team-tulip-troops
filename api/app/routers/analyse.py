import uuid
from fastapi import APIRouter
from pipeline.src import emotion, entities, credibility
from app import schemas
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

router = APIRouter()


def insert_data(index_name, data):
    # Found in the 'Manage this deployment' page
    CLOUD_ID = "3b7c7ef1ec744d898bf05ea60d28d2de:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDVmNWNkY2UyOTFlMjQ3YWE5YjhmMWZlNjgyM2Y2NTE4JDRjOTY5N2YzYmY2ZjQwY2I5MmU4NWNkY2UzNjRlZjU1"

    # Found in the 'Management' page under the section 'Security'
    API_KEY = "ZjNHMFRJWUJETGVSREluRXdLVnY6VGl1d3NPQjdSRWF5aU1aQVRFSkRnQQ=="

    # Create the client instance
    es = Elasticsearch(
        cloud_id=CLOUD_ID,
        api_key=API_KEY,
    )
    actions = []

    
    for row in data:
        doc = {
            "_index": index_name,
            "_id": uuid.uuid4(),
            "_source": row
        }
        actions.append(doc)


    try:
        helpers.bulk(es, actions)
    except helpers.BulkIndexError as bie:
        for error in bie.errors:
            print(error)


@router.post('')
def analyse(body: schemas.GenericRequest):
    claim = body.data

    obj = {
        "id": uuid.uuid4(),
        "datetime": datetime.utcnow(),
        "raw_text":"",
        "sentiment": {},
        "entities": [],
        "credibility_score": 0
    }

    obj['raw_text'] = claim
    claim_obj = {"cleanRenderedContent": claim}

    obj['sentiment'] = emotion.get_sentiment(claim_obj)

    obj['entities'] = entities.get_entities(claim_obj)
    
    obj['credibility'] = credibility.investigate_claim(claim, model_type='zero-shot')

    obj['credibility_score'] = obj['credibility']['credibility_score']

    insert_data('claims1', [obj])

    return obj





@router.get('')
def analyse():
    return {}


@router.get('/{id}')
def analyse(id: str, body: schemas.GenericRequest):
    return {}