from entities.User import User
from database.Database import Database
from sqlalchemy.exc import IntegrityError


class UserService:

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
