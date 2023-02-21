from fastapi import APIRouter
from app import schemas

router = APIRouter()


@router.post('')
def analyse(body: schemas.GenericRequest):
    print(body)

    # EXECUTE ANALYZER


    # INSERT ANALYZER RESULTS IN DB

    return body





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