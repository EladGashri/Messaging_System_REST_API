from typing import *
from flask_restful import Resource
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from flask_jwt_extended import jwt_required, get_jwt_identity


class UnreadMessagesResource(Resource):

    decorators  = [jwt_required()]

    @inject
    def __init__(self,database: Database):
        self.database:Database = database

    def get(self,id:int=None)->Tuple[Dict[str,str],int]:
        user = self.jwtUtils.getUserFromJwt(get_jwt_identity(), self.database)
        if user is not None:
            unreadMessages=[message for message in user.messages if not message.read]
            return {"unread messages":unreadMessages}, HTTPStatusCode.OK.value
        else:
            return {"error": "incorrect JWT"}, HTTPStatusCode.UNAUTHORIZED.value