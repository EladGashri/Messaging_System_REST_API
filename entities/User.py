from dataclasses import dataclass, field
from typing import Dict


# The User class represents the user table in the database using Object Relational Mapping (ORM).
@dataclass
class User:
    username:str = field(default=None)
    password:str = field(default=None)
    name:str = field(default="John Doe")
    
    
    def as_dict(self) -> Dict[str, str]:
        return vars(self)


    @classmethod
    def get_user_from_model(cls, model):
        return cls(model.username, model.name, model.password)