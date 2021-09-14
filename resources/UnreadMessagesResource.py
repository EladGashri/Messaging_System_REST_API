from typing import Tuple, Dict, List, Optional
from flask_restful import Resource
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
        messages:Optional[List[Dict[str,str]]] = Message.getMessageFromJwtIdentity(get_jwt_identity(),self.jwtUtils, self.database)
        if messages is not None:
            unreadMessages:List[Dict[str,str]] = [message for message in messages if not message["read"]]
            for message in unreadMessages:
                self.database.updateMessageToRead(message)
            return {"messages":unreadMessages}, HTTPStatusCode.OK.value
        else:
            return {"error": "incorrect JWT"}, HTTPStatusCode.UNAUTHORIZED.value
