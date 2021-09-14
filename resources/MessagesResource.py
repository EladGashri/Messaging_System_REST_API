from typing import Tuple, Dict, List, Optional
from flask_restful import Resource
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from security.JwtUtils import JwtUtils
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.entities import Message,User


class MessagesResource(Resource):

    decorators  = [jwt_required()]

    @inject
    def __init__(self, database:Database, jwtUtils:JwtUtils) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils


    def get(self) -> Tuple[Dict[str,str],int]:
        messages:Optional[List[Dict[str,str]]] = Message.getMessageFromJwtIdentity(get_jwt_identity(), self.jwtUtils, self.database)
        if messages is not None:
            for message in messages:
                self.database.updateMessageToRead(message)
            return {"messages":messages}, HTTPStatusCode.OK.value
        else:
            return {"error": "incorrect JWT"}, HTTPStatusCode.UNAUTHORIZED.value


    def post(self) -> Tuple[Dict[str, str], int]:
        return {"data": "posted"}, HTTPStatusCode.CREATED.value


    def delete(self, id: int):
        return {"data": "deleted"}, HTTPStatusCode.OK.value
