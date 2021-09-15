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
    def __init__(self, database:Database, jwtUtils:JwtUtils, messageService:MessageService, userService:UserService, resourcesManager:ResourcesManager) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils
        self.messageService:MessageService = messageService
        self.userService:UserService = userService
        self.resourcesManager:ResourcesManager = resourcesManager


    # The endpoint responds to a GET request with all the unread messages sent the user.
    # A second request will not return those messages because after the first request they will all be marked as 'read'.
    def get(self) -> Tuple[Dict[str,str],int]:
        user = self.resourcesManager.getUser(self.userService ,self.database, get_jwt_identity())
        messages = self.messageService.getUserMessages(user, self.database, onlyUnreadMessages=True)
        return {"messages": messages}, HTTPStatusCode.OK.value