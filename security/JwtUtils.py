from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from typing import Dict, Optional
from database.Database import Database
from datetime import timedelta


# The usage of Json Web Token (JWT) for authentication instead of login and sessions allows to preserve the stateless principle in REST.
# the stateless principle in REST is preserved because using by JWT every request is independent from any other request
class JwtUtils:
    SECRET_KEY:str = "dfhg45ytyj67jt7j665j7"
    EXPIRATION_HOURS:int = 12
    JWT_PREFIX:str = "Bearer "
    HEADER:str = "Authorization";


    def __init__(self, app:Flask) -> None:
        app.config["JWT_SECRET_KEY"] = JwtUtils.SECRET_KEY
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=JwtUtils.EXPIRATION_HOURS)
        self.jwt_manager:JWTManager = JWTManager(app)


    def get_jwt(self, username:str, password:str, database:Database) -> Optional[str]:
        if database.get_user(username, password) is not None:
            user_feilds:Dict[str, str] = {"username":username, "password":password}
            return create_access_token(identity=user_feilds)
        else:
            return None