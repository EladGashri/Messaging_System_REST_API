from dataclasses import dataclass, field


@dataclass
class User:
    username:str = field(default=None)
    password:str = field(default=None)
    name:str = field(default="John Doe")

    @classmethod
    def fromModel(cls, model):
        return cls(model.username, model.name, model.password)