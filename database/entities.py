from dataclasses import *
from datetime import date


#The database tables are represented as classes using Object Relational Mapping (ORM)

@dataclass(frozen=True, Order=True)
class Message:
    id:int = field(default=-1)
    senderId:int = field(default=-1)
    receiverId:int = field(default=-1)
    message:str = field(default=None)
    subject:str = field(default=None)
    creationDate:date = field(default=None)
    read:bool = field(default=False)

@dataclass(frozen=True, Order=True)
class User:
    id:int = field(default=-1)
    name:str = field(default="John Doe")