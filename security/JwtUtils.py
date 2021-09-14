from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from typing import Dict, List,Optional
from database.Database import Database
from datetime import timedelta


#The usage of Json Web Token (JWT) for authentication instead of login and sessions aloows to preserve the stateless principle in REST
#because by using JWT every request is independent from any other request
class JwtUtils:
    SECRET_KEY:str = "dfhg45ytyj67jt7j665j7"
    #1 day in milliseconds
    EXPIRATION_HOURS:int = 12
    TOKEN_PREFIX:str = "Bearer "
    HEADER:str = "Authorization";


    def __init__(self, app:Flask) -> None:
        app.config["JWT_SECRET_KEY"] = JwtUtils.SECRET_KEY
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=JwtUtils.EXPIRATION_HOURS)
        self.manager=JWTManager(app)


    def getJwt(self, requestBody:Dict[str,str]) -> Optional[str]:
        if "username" in requestBody and "password" in requestBody:
            userFeilds: Dict[str, str] = dict()
            userFeilds["username"] = requestBody["username"]
            userFeilds["password"] = requestBody["password"]
            return create_access_token(identity=userFeilds)
        else:
            return None


    def getUserFromJwt(self, userFeilds:Optional[Dict[str,str]], database:Database):
        if userFeilds is not None and "username" in userFeilds and "password" in userFeilds:
            username: str = userFeilds["username"]
            password: str = userFeilds["password"]
            print("username: " + username)
            print("username: " + password)
            return database.getUser(username, password)
        else:
            return None