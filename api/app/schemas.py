import typing
from pydantic import BaseModel


class GenericResponse(BaseModel):
    data: typing.Any
    total_records: int
    message: str
    status: str


class GenericRequest(BaseModel):
    data: typing.Any