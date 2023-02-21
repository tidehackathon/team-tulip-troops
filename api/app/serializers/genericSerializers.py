from bson import json_util
import json


def genericResponseEntity(response_object) -> dict:
    response_object = json.loads(json_util.dumps(response_object))
    return {
        "data": response_object['data'],
        "total_records": response_object['total_records'],
        "message": response_object['message'],
        "status": response_object['status']
    }


def genericRequestEntity(request_object) -> dict:
    return {
        request_object
    }
