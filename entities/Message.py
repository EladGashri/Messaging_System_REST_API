from dataclasses import dataclass, field
from typing import ClassVar, Dict
from datetime import date


# The Message class represents the message table in the database using Object Relational Mapping (ORM).
@dataclass
class Message:
    last_message_id:ClassVar[int]
    id:int = field(default=-1)
    sender_username:str = field(default=None)
    receiver_username:str = field(default=None)
    subject:str = field(default=None)
    message:str = field(default=None)
    creation_date:str = field(default=str(date.today()))
    read:bool = field(default=False)


    def as_dict(self) -> Dict[str, str]:
        return vars(self)


    @classmethod
    def get_message_from_model(cls, model):
        return cls(model.id, model.sender_username, model.receiver_username, model.message, model.subject, str(model.creation_date), model.read)


    @classmethod
    def increment_last_message_id(cls) -> None:
        setattr(cls, "last_message_id", cls.last_message_id + 1)