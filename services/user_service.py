from entities.user import User
from typing import Dict, Optional
from database.database import Database
from sqlalchemy.exc import IntegrityError


# The UserService class contains the buisness logic related to the user table in the database
class UserService:


    def get_user_from_jwt(self, user_feilds:Optional[Dict[str,str]], database:Database):
        if user_feilds is not None and "username" in user_feilds and "password" in user_feilds:
            username:str = user_feilds["username"]
            password:str = user_feilds["password"]
            return database.get_user(username, password)
        else:
            return None


    def insert_user(self, database:Database, username:str, password:str, name:str) -> bool:
        user:User = User(username, password, name)
        try:
            database.insert_new_user(user)
            return True
        except IntegrityError as integrity_error:
            print(integrity_error)
            return False


    def check_username(self,database:Database, username:str) -> bool:
        return database.get_user(username) is not None
