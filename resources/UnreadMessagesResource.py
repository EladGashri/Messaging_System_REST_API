from typing import Tuple, Dict
from flask_restful import Resource, abort
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.entities import Message
from security.JwtUtils import JwtUtils


class UnreadMessagesResource(Resource):

    decorators  = [jwt_required()]

    @inject
    def __init__(self, database:Database, jwtUtils:JwtUtils) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils


    def get(self) -> Tuple[Dict[str,str],int]:
        user = self._getUser(get_jwt_identity())
        messages = Message.getUserMessages(user, self.database, onlyUnreadMessages=True)
        return {"messages": messages}, HTTPStatusCode.OK.value


    def _getUser(self, jwtIdentity:str):
        user = self.jwtUtils.getUserFromJwt(jwtIdentity, self.database)
        if user is not None:
            return user
        else:
            abort(HTTPStatusCode.UNAUTHORIZED.value, error="username or password incorrect")