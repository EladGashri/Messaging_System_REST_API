from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from typing import Dict, List,Optional
from database.Database import Database
from flask_injector import inject
from datetime import timedelta


#The usage of Json Web Token (JWT) for authentication instead of login and sessions aloows to preserve the stateless principle in REST
#because by using JWT every request is independent from any other request
class JwtUtils:
    SECRET_KEY:str = "dfhg45ytyj67jt7j665j7"
    #1 day in milliseconds
    EXPIRATION_HOURS:int = 1
    TOKEN_PREFIX:str = "Bearer "
    HEADER:str = "Authorization";
    USER_FIELDS_FOR_JWT:List[str] = ["username", "password"]

    @inject
    def __init__(self, app:Flask, database:Database) -> None:
        app.config["JWT_SECRET_KEY"] = JwtUtils.SECRET_KEY
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=JwtUtils.EXPIRATION_HOURS)
        self.manager=JWTManager(app)
        self.database:Database = database


    def getJwt(self, requestBody:Dict[str,str]) -> Optional[str]:
        userFeilds:Optional[Dict[str,str]] = self._getUserFeilds(requestBody)
        return create_access_token(identity=userFeilds)


    def getUserFromJwt(self, requestHeader:Dict[str,str]):
        jwt:str = requestHeader.get("jwt")
        if jwt is not None:
            return self.database.getUser(get_jwt_identity(jwt))
        else:
            return None


    def _getUserFeilds(self, request:Dict[str,str])->Optional[Dict[str,str]]:
        userFeilds:Dict[str,str] = dict()
        for feild in JwtUtils.USER_FIELDS_FOR_JWT:
            if feild in request:
                userFeilds[feild]=request.get(feild)
            else:
                return None