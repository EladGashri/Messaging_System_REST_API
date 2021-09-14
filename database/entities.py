from dataclasses import *
from security.JwtUtils import JwtUtils
from database.Database import Database
from typing import Dict, List, Optional
from datetime import date


#The database tables are represented as classes using Object Relational Mapping (ORM)

@dataclass
class Message:
    id:int = field(default=-1)
    senderUsername:str = field(default=None)
    receiverUsername:str = field(default=None)
    message:str = field(default=None)
    subject:str = field(default=None)
    creationDate:str = field(default=str(date.today()))
    read:bool = field(default=False)


    @classmethod
    def getMessagefromModel(cls, model):
        return cls(model.id, model.senderUsername, model.receiverUsername, model.message, model.subject, str(model.creationDate))


    @classmethod
    def getMessage(cls, messageId:int, user, database:Database):
        message = database.getMessage(messageId, user)
        if message is not None:
            database.updateMessageToRead(message)
            return cls.getMessagefromModel(message)._getMessageAsDict()
        else:
            return None


    @classmethod
    def getUserMessages(cls, user, database:Database, onlyUnreadMessages :bool = False) -> Optional[List[Dict[str,str]]]:
        if onlyUnreadMessages:
            messages=[message for message in user.receivedMessages if not message.read]
        else:
            messages=user.receivedMessages
        for message in messages:
            if not message.read:
                database.updateMessageToRead(message)
        return [cls.getMessagefromModel(message)._getMessageAsDict() for message in messages]


    def _getMessageAsDict(self)->Dict[str, str]:
        return vars(self)


@dataclass
class User:
    username:str = field(default=None)
    password:str = field(default=None)
    name:str = field(default="John Doe")

    @classmethod
    def fromModel(cls, model):
        return cls(model.username, model.name, model.password)