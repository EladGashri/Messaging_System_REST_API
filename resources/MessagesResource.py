from typing import Tuple, Dict
from flask import request
from flask_restful import Resource, abort
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from security.JwtUtils import JwtUtils
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.MessageService import MessageService
from services.UserService import UserService
from resources.ResourcesManager import ResourcesManager


#the MessagesResource represented the endpoint with the URI /messaging-system/messages.
class MessagesResource(Resource):


    decorators  = [jwt_required()]


    @inject
    def __init__(self, database:Database, jwtUtils:JwtUtils, messageService:MessageService, userService:UserService, resourcesManager:ResourcesManager) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils
        self.messageService:MessageService = messageService
        self.userService:UserService = userService
        self.resourcesManager:ResourcesManager = resourcesManager


    # The endpoint responds to a GET request with one of the following:
    #1. A specific message sent to the user if he put a message-id as a query parameter.
    #2. All the messages sent the user if he didn't put a message-id as a query parameter.
    def get(self) -> Tuple[Dict[str,str],int]:
        user = self.resourcesManager.getUser(self.userService ,self.database, get_jwt_identity())
        messageId:int = self.resourcesManager.getMessageId()
        if messageId is not None:
            message = self.messageService.getMessage(messageId, user, self.database)
            if message is not None:
                return {"message": message}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.NOT_FOUND.value, error="message not found")
        else:
            messages = self.messageService.getUserMessages(user, self.database)
            return {"messages": messages}, HTTPStatusCode.OK.value


    # In order to write a message A POST request sould be sent to the endpoint with the receiver-username, subject and message in the request body.
    def post(self) -> Tuple[Dict[str, str], int]:
        requestBody:Dict[str,str] =request.get_json()
        if "receiver-username" in requestBody and "subject" in requestBody and "message" in requestBody:
            if self.userService.checkUsername(self.database, requestBody["receiver-username"]):
                user = self.resourcesManager.getUser(self.userService, self.database, get_jwt_identity())
                messageId:int = self.messageService.insertMessage(user.username, requestBody["receiver-username"], requestBody["subject"], requestBody["message"], self.database)
                return {"information": f"message posted with message id {messageId}"}, HTTPStatusCode.CREATED.value
            else:
                receiverUsername:str = requestBody["receiver-username"]
                abort(HTTPStatusCode.BAD_REQUEST.value,error=f"no username {receiverUsername}")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit receiver-username, subject and message in the request body")

    # A DELETE request to the endpoint deletes the message with the message-id sent in the query parameter (if that message was send from or to the user)
    def delete(self):
        user = self.resourcesManager.getUser(self.userService ,self.database, get_jwt_identity())
        messageId:int = self.resourcesManager.getMessageId()
        if messageId is not None:
            deleted:bool = self.messageService.deleteMessage(messageId, user, self.database)
            if deleted:
                return {"information": "message deleted"}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.NOT_FOUND.value, error="message not found")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit message-id as query parameters")