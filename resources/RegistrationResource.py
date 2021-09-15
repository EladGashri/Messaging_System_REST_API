from typing import Tuple, Dict
from flask import request
from flask_restful import Resource, abort
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from services.UserService import UserService
from resources.ResourcesManager import ResourcesManager


# The RegistrationResource represented the endpoint with the URI /messaging-system/registration
class RegistrationResource(Resource):


    @inject
    def __init__(self, database:Database, userService:UserService, resourcesManager:ResourcesManager) -> None:
        self.database:Database = database
        self.userService:UserService = userService
        self.resourcesManager:ResourcesManager = resourcesManager


    # In order to register a new user message A POST request sould be sent to the endpoint with the sername, password and name in the request body.
    # The username should not already belong to another user.
    def post(self) -> Tuple[Dict[str,str],int]:
        requestBody:Dict[str,str] = self.resourcesManager.getRequestBody(request)
        if "username" in requestBody and "password" in requestBody and "name" in requestBody:
            inserted:bool = self.userService.insertUser(self.database, requestBody["username"], requestBody["password"], requestBody["name"])
            username: str = requestBody["username"]
            if inserted:
                return {"information": f"user {username} registered"}, HTTPStatusCode.CREATED.value
            else:
                abort(HTTPStatusCode.BAD_REQUEST.value, error=f"username {username} already belongs to another user")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit username, password and name in the request body")
