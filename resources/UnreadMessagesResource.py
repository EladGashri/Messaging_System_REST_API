from typing import *
from flask import request
from flask_restful import Resource
from flask_injector import inject
from http_codes.HTTPStatusCode import HTTPStatusCode
from database.Database import Database
from flask_jwt_extended import jwt_required


class UnreadMessagesResource(Resource):

    method_decorators = [jwt_required()]

    @inject
    def __init__(self,database: Database):
        self.database:Database = database

    def get(self,id:int=None)->Tuple[Dict[str,str],int]:
        return {"data":"Messages"},HTTPStatusCode.OK.value