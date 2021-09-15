from flask import Flask
from abc import ABC, abstractmethod
from entities.message import Message
from entities.user import User


# Database is an abstract class that represents a general interface for a database for this REST API.
class Database(ABC):
    DATABASE_NAME:str = "Messaging_System.db"
    DATABASE_PATH:str = f"sqlite:///{DATABASE_NAME}"
    SECRET_KEY:str = "psjtk40gk5kf0orr9k3ns"

    @abstractmethod
    def insert_new_message(self, message:Message) -> None:
        pass

    @abstractmethod
    def insert_new_user(self, user:User) -> None:
        pass

    @abstractmethod
    def get_message(self, id: int, user, also_sender:bool):
        pass

    @abstractmethod
    def get_user(self, username:str, password:str):
        pass

    @abstractmethod
    def update_message_to_read(self, message)->None:
        pass

    @abstractmethod
    def delete_message(self, message)->None:
        pass

    @abstractmethod
    def delete_database(self)->None:
        pass

    @abstractmethod
    def _config(self, app:Flask)->None:
        pass

    @abstractmethod
    def _create_message_table(self):
        pass

    @abstractmethod
    def _create_user_table(self):
        pass

    @abstractmethod
    def _set_last_message_id(self)-> None:
        pass