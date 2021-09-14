from dataclasses import *
from security.JwtUtils import JwtUtils
from database.Database import Database
from typing import Dict, List, Optional


#The database tables are represented as classes using Object Relational Mapping (ORM)

@dataclass
class Message:
    id:int = field(default=-1)
    sender_username:str = field(default=None)
    receiver_username:str = field(default=None)
    message:str = field(default=None)
    subject:str = field(default=None)
    creation_date:str = field(default=None)
    read:bool = field(default=False)

    @classmethod
    def getMessagefromModel(cls, model):
        return cls(model.id, model.senderUsername, model.receiverUsername, model.message, model.subject, str(model.creationDate), model.read)

    @classmethod
    def getMessageFromJwtIdentity(cls, jwtIdentity:str, jwtUtils:JwtUtils, database:Database, onlyReceivedMessages:bool =True) -> Optional[List[Dict[str,str]]]:
        user = jwtUtils.getUserFromJwt(jwtIdentity, database)
        if user is not None:
            if onlyReceivedMessages:
                messages=user.receivedMessages
            else:
                messages=list(set(user.receivedMessages + user.sentMessages))
            return [vars(cls.getMessagefromModel(message)) for message in messages]
        else:
            return None


@dataclass
class User:
    username:str = field(default=None)
    name:str = field(default="John Doe")

    @classmethod
    def fromModel(cls, model):
        return cls(model.username, model.name)