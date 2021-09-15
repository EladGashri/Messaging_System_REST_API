from typing import Tuple, Dict, Optional
from flask import request
from flask_restful import Resource, abort
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from security.JwtUtils import JwtUtils
from resources.ResourcesManager import ResourcesManager
from services.MessageService import MessageService
from services.UserService import UserService



# The AuthenticationResource represented the endpoint with the URI /messaging-system/authentication.
class AuthenticationResource(Resource):


    @inject
    def __init__(self, database:Database, jwt_utils:JwtUtils, message_service:MessageService, user_service:UserService, resources_manager:ResourcesManager) -> None:
        self.database:Database = database
        self.jwt_utils:JwtUtils = jwt_utils
        self.message_service:MessageService = message_service
        self.user_service:UserService = user_service
        self.resources_manager:ResourcesManager = resources_manager


    # The endpoint responds to a POST request with a JWT if the user is in the database.
    # The user needs to submit hit username and password in the request body.
    def post(self) -> Tuple[Dict[str,str],int]:
        request_body:Dict[str,str] = request.get_json()
        if "username" in request_body and "password" in request_body:
            jwt:Optional[str] = self.jwt_utils.get_jwt(request_body["username"], request_body["password"], self.database)
            if jwt is not None:
                return {"jwt":jwt}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.UNAUTHORIZED.value, error="incorrect username or password")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit username and password in the request body")