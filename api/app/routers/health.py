from fastapi import APIRouter, Request, Header
from datetime import datetime

router = APIRouter()


@router.get('')
def health(request: Request, user_agent: str = Header(default=None)):
    return {
        "status": "online",
        "server_time": datetime.now(),
        "client_host": request.client.host,
        "user_agent": 'user_agent'
    }