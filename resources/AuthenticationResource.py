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
    def __init__(self, database:Database, jwtUtils:JwtUtils, messageService:MessageService, userService:UserService, resourcesManager:ResourcesManager) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils
        self.messageService:MessageService = messageService
        self.userService:UserService = userService
        self.resourcesManager:ResourcesManager = resourcesManager


    # The endpoint responds to a POST request with a JWT if the user is in the database.
    # The user needs to submit hit username and password in the request body.
    def post(self) -> Tuple[Dict[str,str],int]:
        requestBody:Dict[str,str] = request.get_json()
        if "username" in requestBody and "password" in requestBody:
            jwt:Optional[str] = self.jwtUtils.getJwt(requestBody["username"], requestBody["password"], self.database)
            if jwt is not None:
                return {"jwt":jwt}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.UNAUTHORIZED.value, error="incorrect username or password")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit username and password in the request body")