from dataclasses import dataclass, field
from typing import ClassVar, Dict
from datetime import date


#The database tables are represented as classes using Object Relational Mapping (ORM)

@dataclass
class Message:
    numberOfMessages:ClassVar[int]
    id:int = field(default=-1)
    senderUsername:str = field(default=None)
    receiverUsername:str = field(default=None)
    subject:str = field(default=None)
    message:str = field(default=None)
    creationDate:str = field(default=str(date.today()))
    read:bool = field(default=False)


    def getMessageAsDict(self)->Dict[str, str]:
        return vars(self)


    @classmethod
    def getMessagefromModel(cls, model):
        return cls(model.id, model.senderUsername, model.receiverUsername, model.message, model.subject, str(model.creationDate), model.read)


    @classmethod
    def incrementNumberOfMesages(cls) -> None:
        setattr(cls, "numberOfMessages", cls.numberOfMessages + 1)