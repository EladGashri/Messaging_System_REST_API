from typing import Tuple, Dict
from flask import request
from flask_restful import Resource, reqparse, abort
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
        self.requestParser=reqparse.RequestParser()
        self.requestParser.add_argument("message-id", type=int, required=False)


    def get(self) -> Tuple[Dict[str,str],int]:
        user = self._getUser(get_jwt_identity())
        messageId: int = self.requestParser.parse_args().get("message-id", None)
        if messageId is not None:
            message = Message.getMessage(messageId, user, self.database)
            if message is not None:
                return {"message": message}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.NOT_FOUND.value, error="message not found")
        else:
            messages = Message.getUserMessages(user, self.database)
            return {"messages": messages}, HTTPStatusCode.OK.value


    def post(self) -> Tuple[Dict[str, str], int]:
        if "send-to" in request.get_json() and "subject" in request.get_json() and "message" in request.get_json():
            Message.writeMessage(request.get_json()["send-to"], request.get_json()["subject"], request.get_json()["message"])
            return {"information": "message posted"}, HTTPStatusCode.CREATED.value
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit send-to, subject and message in the request body")


    def delete(self):
        user = self._getUser(get_jwt_identity())
        messageId: int = self.requestParser.parse_args().get("message-id", None)
        if messageId is not None:
            deleted:bool = Message.deleteMessage(messageId, user, self.database)
            if deleted:
                return {"information": "message deleted"}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.NOT_FOUND.value, error="message not found")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit message-id as query parameters")


    def _getUser(self, jwtIdentity:str):
        user = self.jwtUtils.getUserFromJwt(jwtIdentity, self.database)
        if user is not None:
            return user
        else:
            abort(HTTPStatusCode.UNAUTHORIZED.value, error="username or password incorrect")

