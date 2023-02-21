from fastapi import APIRouter
from pipeline.src import emotion, entities
from app import schemas

router = APIRouter()


@router.post('')
def analyse(body: schemas.GenericRequest):
    claim = body.data

    obj = {
        "id": "111",
        "raw_text":"",
        "summary": "",
        "sentiment": {},
        "five_ws": {
            "Who":"ChatGPT",
            "What":"controversial",
            "When":"",
            "Where":"",
            "Why":""
        },
        "search_confidence": 0.7877,
        "entities": [
            {
                "text":"Google Inc.",
                "label": "ORG"
            },
            {
                "text":"Elon Musk",
                "label": "PERSON"
            },
            {
                "text":"California",
                "label": "GPE"
            }
        ],
        "credibility_score": 0.7345
    }

    obj['raw_text'] = claim
    claim_obj = {"cleanRenderedContent": claim}
    obj['sentiment'] = emotion.get_sentiment(claim_obj)

    print(entities.get_entities(claim_obj))
    

    # print(credibility.investigate_claim(claim, model_type='zero-shot'))

    # print(entities.get_entities())


    # obj['sentiment'] = emotion.get_sentiment(claim)
    

    

    
    # EXECUTE ANALYZER


    # INSERT ANALYZER RESULTS IN DB

    return obj





@router.get('')
def analyse():
    data = [
        {
            "id": "1234987128743",
            "raw_text":"ChatGPT lists Trump, Elon Musk as controversial and worthy of special treatment, Biden and Bezos as not.",
            "summary": "",
            "sentiment": [
                {
                    "label":"POSITIVE",
                    "score": 0.98273
                },
                {
                    "label":"NEGATIVE",
                    "score": 0.98273
                }
            ],
            "five_ws": {
                "Who":"ChatGPT",
                "What":"controversial",
                "When":"",
                "Where":"",
                "Why":""
            },
            "search_confidence": 0.7877,
            "entities": [
                {
                    "text":"Google Inc.",
                    "label": "ORG"
                },
                {
                    "text":"Elon Musk",
                    "label": "PERSON"
                },
                {
                    "text":"California",
                    "label": "GPE"
                }
            ],
            "score": 0.7345
        }
    ]


    return data


@router.get('/{id}')
def analyse(id: str, body: schemas.GenericRequest):



    return {}