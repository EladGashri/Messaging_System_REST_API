from typing import Tuple, Dict
from flask import request
from flask_restful import Resource, abort
#from flask_injector import inject
from http_status_codes.http_status_code import HTTPStatusCode
from database.database import Database
from services.user_service import UserService


# The RegistrationResource represented the endpoint with the URI /registration.
class RegistrationResource(Resource):


    #@inject
    def __init__(self, database:Database, user_service:UserService) -> None:
        self.database:Database = database
        self.user_service:UserService = user_service


    # In order to register a new user message A POST request sould be sent to the endpoint with the sername, password and name in the request body.
    # The username should not already belong to another user.
    def post(self) -> Tuple[Dict[str,str],int]:
        request_body:Dict[str,str] = request.get_json()
        if "username" in request_body and "password" in request_body and "name" in request_body:
            inserted:bool = self.user_service.insert_user(self.database, request_body["username"], request_body["password"], request_body["name"])
            username: str = request_body["username"]
            if inserted:
                return {"information": f"user {username} registered"}, HTTPStatusCode.CREATED.value
            else:
                abort(HTTPStatusCode.BAD_REQUEST.value, error=f"username {username} already belongs to another user")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit username, password and name in the request body")