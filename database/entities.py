from dataclasses import dataclass, field
#from database.Database import Database
from typing import ClassVar, Dict, List, Optional
from datetime import date


#The database tables are represented as classes using Object Relational Mapping (ORM)

@dataclass
class Message:
    numberOfMessages:ClassVar[int] = 5
    id:int = field(default=-1)
    senderUsername:str = field(default=None)
    receiverUsername:str = field(default=None)
    subject:str = field(default=None)
    message:str = field(default=None)
    creationDate:str = field(default=str(date.today()))
    read:bool = field(default=False)


    @classmethod
    def getMessagefromModel(cls, model):
        return cls(model.id, model.senderUsername, model.receiverUsername, model.message, model.subject, str(model.creationDate), model.read)


    @classmethod
    def getMessage(cls, messageId:int, user, database):
        message = database.getMessage(messageId, user)
        if message is not None:
            database.updateMessageToRead(message)
            return cls.getMessagefromModel(message)._getMessageAsDict()
        else:
            return None


    @classmethod
    def getUserMessages(cls, user, database, onlyUnreadMessages :bool = False) -> Optional[List[Dict[str,str]]]:
        if onlyUnreadMessages:
            messages=[message for message in user.receivedMessages if not message.read]
        else:
            messages=user.receivedMessages
        messagesAsDicts = [cls.getMessagefromModel(message)._getMessageAsDict() for message in messages]
        for message in messages:
            if not message.read:
                database.updateMessageToRead(message)
        return messagesAsDicts

    @classmethod
    def deleteMessage(self, messageId:int, user, database) -> bool:
        message = database.getMessage(messageId, user, alsoSender=True)
        if message is not None:
            database.deleteMessage(message)
            return True
        else:
            return False


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