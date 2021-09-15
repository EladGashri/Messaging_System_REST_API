from dataclasses import dataclass, field
from typing import Dict
from entities.User import User


#The User class represents the user table in the database using Object Relational Mapping (ORM)

@dataclass
class User:
    username:str = field(default=None)
    password:str = field(default=None)
    name:str = field(default="John Doe")
    
    
    def getUserAsDict(self) -> Dict[str, str]:
        return vars(self)


    @classmethod
    def fromModel(cls, model) -> User:
        return cls(model.username, model.name, model.password)