from flask import abort
from http_codes.HTTPStatusCode import HTTPStatusCode
from services.UserService import UserService
from typing import Optional
from database.Database import Database
from flask_restful.reqparse import RequestParser


# The ResourcesManager stores the logic that is shared by all the resource classes
class ResourcesManager:


    def get_user(self, user_service:UserService, database:Database, jwt_identity:str):
        user = user_service.get_user_from_jwt(jwt_identity, database)
        if user is not None:
            return user
        else:
            abort(HTTPStatusCode.UNAUTHORIZED.value, error="invalid JWT")


    def get_message_id(self) -> Optional[int]:
        request_parser:RequestParser = RequestParser()
        request_parser.add_argument("message-id", type=int, required=False)
        return request_parser.parse_args().get("message-id", None)