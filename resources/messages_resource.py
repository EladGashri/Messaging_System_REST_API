from typing import Tuple, Dict
from flask import request
from flask_restful import Resource, abort
from http_status_codes.http_status_code import HTTPStatusCode
from database.database import Database
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.message_service import MessageService
from services.user_service import UserService
from resources.resources_manager import ResourcesManager


#the MessagesResource represented the endpoint with the URI /messages.
class MessagesResource(Resource):


    decorators  = [jwt_required()]


    def __init__(self, database:Database, message_service:MessageService, user_service:UserService, resources_manager:ResourcesManager) -> None:
        self.database:Database = database
        self.message_service:MessageService = message_service
        self.user_service:UserService = user_service
        self.resources_manager:ResourcesManager = resources_manager


    # The endpoint responds to a GET request with one of the following:
    #1. A specific message sent to the user if he put a message-id as a query parameter.
    #2. All the messages sent the user if he didn't put a message-id as a query parameter.
    def get(self) -> Tuple[Dict[str,str],int]:
        user = self.resources_manager.get_user(self.user_service ,self.database, get_jwt_identity())
        message_id:int = self.resources_manager.get_message_id()
        if message_id is not None:
            message = self.message_service.get_message(message_id, user, self.database)
            if message is not None:
                return {"message": message}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.NOT_FOUND.value, error="message not found")
        else:
            messages = self.message_service.get_user_messages(user, self.database)
            return {"messages": messages}, HTTPStatusCode.OK.value


    # In order to write a message A POST request sould be sent to the endpoint with the receiver-username, subject and message in the request body.
    def post(self) -> Tuple[Dict[str, str], int]:
        request_body:Dict[str,str] =request.get_json()
        if "receiver-username" in request_body and "subject" in request_body and "message" in request_body:
            if self.user_service.check_username(self.database, request_body["receiver-username"]):
                user = self.resources_manager.get_user(self.user_service, self.database, get_jwt_identity())
                message_id:int = self.message_service.insert_message(user.username, request_body["receiver-username"], request_body["subject"], request_body["message"], self.database)
                return {"information": f"message posted with message id {message_id}"}, HTTPStatusCode.CREATED.value
            else:
                receiver_username:str = request_body["receiver-username"]
                abort(HTTPStatusCode.BAD_REQUEST.value,error=f"no username {receiver_username}")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit receiver-username, subject and message in the request body")

    # A DELETE request to the endpoint deletes the message with the message-id sent in the query parameter (if that message was send from or to the user)
    def delete(self):
        user = self.resources_manager.get_user(self.user_service ,self.database, get_jwt_identity())
        message_id:int = self.resources_manager.get_message_id()
        if message_id is not None:
            deleted:bool = self.message_service.delete_message(message_id, user, self.database)
            if deleted:
                return {"information": "message deleted"}, HTTPStatusCode.OK.value
            else:
                abort(HTTPStatusCode.NOT_FOUND.value, error="message not found")
        else:
            abort(HTTPStatusCode.BAD_REQUEST.value, error="must submit message-id as query parameters")