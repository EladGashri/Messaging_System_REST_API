from entities.User import User
from typing import Dict, Optional
from database.Database import Database
from sqlalchemy.exc import IntegrityError


# The UserService class contains the buisness logic related to the user table in the database
class UserService:


    def getUserFromJwt(self, userFeilds:Optional[Dict[str,str]], database:Database):
        if userFeilds is not None and "username" in userFeilds and "password" in userFeilds:
            username: str = userFeilds["username"]
            password: str = userFeilds["password"]
            return database.getUser(username, password)
        else:
            return None


    def insertUser(self, database:Database, username:str, password:str, name:str) -> bool:
        user:User = User(username, password, name)
        try:
            database.insertNewUser(user)
            return True
        except IntegrityError as e:
            print(e)
            return False


    def checkUsername(self,database:Database, username:str) -> bool:
        return database.getUser(username) is not None
