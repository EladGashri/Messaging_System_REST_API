from typing import Tuple, Dict
from flask_restful import Resource, abort
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from flask_jwt_extended import jwt_required, get_jwt_identity
from security.JwtUtils import JwtUtils
from services.MessageService import MessageService
from services.UserService import UserService


class UnreadMessagesResource(Resource):

    decorators  = [jwt_required()]

    @inject
    def __init__(self, database:Database, jwtUtils:JwtUtils, messageService:MessageService, userService:UserService) -> None:
        self.database:Database = database
        self.jwtUtils:JwtUtils = jwtUtils
        self.messageService:MessageService = messageService
        self.userService:UserService = userService


    def get(self) -> Tuple[Dict[str,str],int]:
        user = self._getUser(get_jwt_identity())
        messages = self.messageService.getUserMessages(user, self.database, onlyUnreadMessages=True)
        return {"messages": messages}, HTTPStatusCode.OK.value


    def _getUser(self, jwtIdentity:str):
        user = self.userService.getUserFromJwt(jwtIdentity, self.database)
        if user is not None:
            return user
        else:
            abort(HTTPStatusCode.UNAUTHORIZED.value, error="username or password incorrect")