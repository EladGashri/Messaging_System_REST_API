from typing import Tuple, Dict
from flask import request
from flask_restful import Resource, abort
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from services.UserService import UserService


class RegistrationResource(Resource):

    @inject
    def __init__(self, database:Database, userService:UserService) -> None:
        self.database:Database = database
        self.userService:UserService = userService

    def post(self) -> Tuple[Dict[str,str],int]:
        if "username" in request.get_json() and "password" in request.get_json() and "name" in request.get_json():
            inserted:bool = self.userService.insertUser(self.database, request.get_json()["username"], request.get_json()["password"], request.get_json()["name"])
            username: str = request.get_json()["username"]
            if inserted:
                return {"information": f"user {username} registered"}, HTTPStatusCode.CREATED.value
            else:
                abort(HTTPStatusCode.BAD_REQUEST.value, error=f"username {username} already exists")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit username, password and name in the request body")