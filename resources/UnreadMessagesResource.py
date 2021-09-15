from typing import Tuple, Dict
from flask_restful import Resource
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from flask_jwt_extended import jwt_required, get_jwt_identity
from security.JwtUtils import JwtUtils
from services.MessageService import MessageService
from services.UserService import UserService
from resources.ResourcesManager import ResourcesManager


# The UnreadMessagesResource represented the endpoint with the URI /messaging-system/messages/unread
class UnreadMessagesResource(Resource):


    decorators  = [jwt_required()]


    @inject
    def __init__(self, database:Database, jwt_utils:JwtUtils, message_service:MessageService, user_service:UserService, resources_manager:ResourcesManager) -> None:
        self.database:Database = database
        self.jwt_utils:JwtUtils = jwt_utils
        self.message_service:MessageService = message_service
        self.user_service:UserService = user_service
        self.resources_manager:ResourcesManager = resources_manager


    # The endpoint responds to a GET request with all the unread messages sent the user.
    # A second request will not return those messages because after the first request they will all be marked as 'read'.
    def get(self) -> Tuple[Dict[str,str],int]:
        user = self.resources_manager.get_user(self.user_service ,self.database, get_jwt_identity())
        messages = self.message_service.get_user_messages(user, self.database, only_unread_messages=True)
        return {"messages": messages}, HTTPStatusCode.OK.value