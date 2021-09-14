from typing import Tuple, Dict, Optional
from flask import request
from flask_restful import Resource, abort
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
        if "username" in request.get_json() and "password" in request.get_json():
            jwt:Optional[str] = self.jwtUtils.getJwt(request.get_json()["username"], request.get_json()["password"], self.database)
            if jwt is not None:
                return {"jwt":jwt}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.UNAUTHORIZED.value, error="incorrect username or password")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit username and password in the request body")