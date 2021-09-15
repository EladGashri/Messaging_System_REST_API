from flask import abort
from http_codes.HTTPStatusCode import HTTPStatusCode
from services.UserService import UserService
from typing import Dict, Optional
from database.Database import Database
from flask_restful.reqparse import RequestParser


# The ResourcesManager stores the logic that is shared by all the resource classes
class ResourcesManager:


    def getUser(self, userService:UserService, database:Database, jwtIdentity:str):
        user = userService.getUserFromJwt(jwtIdentity, database)
        if user is not None:
            return user
        else:
            abort(HTTPStatusCode.UNAUTHORIZED.value, error="invalid JWT")


    def getMessageId(self) -> Optional[int]:
        requestParser:RequestParser = RequestParser()
        requestParser.add_argument("message-id", type=int, required=False)
        return requestParser.parse_args().get("message-id", None)


    def getRequestBody(self, request) -> Dict[str,str] :
        return request.get_json()