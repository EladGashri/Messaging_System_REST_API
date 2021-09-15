from typing import Tuple, Dict
from flask import request
from flask_restful import Resource, abort
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from resources.ResourcesManager import ResourcesManager
from services.MessageService import MessageService
from services.UserService import UserService
from security.JwtUtils import JwtUtils



# The RegistrationResource represented the endpoint with the URI /messaging-system/registration
class RegistrationResource(Resource):


    @inject
    def __init__(self, database:Database, jwt_utils:JwtUtils, message_service:MessageService, user_service:UserService, resources_manager:ResourcesManager) -> None:
        self.database:Database = database
        self.jwt_utils:JwtUtils = jwt_utils
        self.message_service:MessageService = message_service
        self.user_service:UserService = user_service
        self.resources_manager:ResourcesManager = resources_manager


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