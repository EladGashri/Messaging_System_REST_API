from typing import Tuple, Dict
from flask_restful import Resource
from flask_injector import inject
from http_status_codes.http_status_code import HTTPStatusCode
from database.database import Database
from flask_jwt_extended import jwt_required, get_jwt_identity
from security.jwt_utils import JwtUtils
from services.message_service import MessageService
from services.user_service import UserService
from resources.resources_manager import ResourcesManager


# The UnreadMessagesResource represented the endpoint with the URI /messages/unread.
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