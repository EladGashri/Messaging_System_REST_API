from typing import Tuple, Dict, Optional
from flask import request
from flask_restful import Resource, abort
from http_status_codes.http_status_code import HTTPStatusCode
from database.database import Database
from security.jwt_utils import JwtUtils


# The AuthenticationResource represented the endpoint with the URI /authentication.
class AuthenticationResource(Resource):


    def __init__(self, database:Database, jwt_utils:JwtUtils) -> None:
        self.database:Database = database
        self.jwt_utils:JwtUtils = jwt_utils


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