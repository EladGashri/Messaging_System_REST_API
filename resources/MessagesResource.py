from typing import *
from flask import make_response, jsonify
from flask_restful import Resource
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from security.JwtUtils import JwtUtils
from flask_jwt_extended import jwt_required, get_jwt_identity


class MessagesResource(Resource):

    decorators  = [jwt_required()]

    @inject
    def __init__(self, database:Database, jwtUtils:JwtUtils) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils

    def post(self) -> Tuple[Dict[str, str], int]:
        return {"data": "Posted"}, HTTPStatusCode.CREATED.value

    def delete(self, id: int):
        return {"data": "Deleted"}, HTTPStatusCode.OK.value

    def get(self)->Tuple[Dict[str,str],int]:
        user = self.jwtUtils.getUserFromJwt(get_jwt_identity(), self.database)
        if user is not None:
            print("hello " + user.name)
            return {"messages":user.messages},HTTPStatusCode.OK.value
        else:
            return {"error": "incorrect JWT"}, HTTPStatusCode.UNAUTHORIZED.value
