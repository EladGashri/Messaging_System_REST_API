from typing import *
from flask import request
from flask_restful import Resource
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from security.JwtUtils import JwtUtils


class AuthenticationResource(Resource):

    @inject
    def __init__(self, database:Database, jwtUtils:JwtUtils) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils

    def post(self) -> Tuple[Dict[str,str],int]:
        jwt:str = self.jwtUtils.getJwt(request.get_json(), self.database)
        if jwt is not None:
            return {"jwt":jwt}, HTTPStatusCode.OK.value
        else:
            return {"error": "must submit username and password in request body"}, HTTPStatusCode.BAD_REQUEST.value