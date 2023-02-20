from fastapi import APIRouter
from app import schemas

router = APIRouter()


@router.post('')
def analyze(body: schemas.GenericRequest):
    print(body)

    # EXECUTE ANALYZER


    # INSERT ANALYZER RESULTS IN DB

    return body