from flask import Flask
from abc import ABC, abstractmethod
from entities.Message import Message
from entities.User import User


# Database is an abstract class that represents a general interface for a database for this REST API.
class Database(ABC):
    DATABASE_NAME:str = "Messaging_System.db"
    DATABASE_PATH:str = f"sqlite:///{DATABASE_NAME}"
    SECRET_KEY:str = "psjtk40gk5kf0orr9k3ns"

    @abstractmethod
    def insertNewMessage(self, message:Message) -> None:
        pass

    @abstractmethod
    def insertNewUser(self, user:User) -> None:
        pass

    @abstractmethod
    def getNumberOfMessages(self) -> int:
        pass

    @abstractmethod
    def getMessage(self, id: int, user, alsoSender:bool):
        pass

    @abstractmethod
    def getUser(self, username:str, password:str):
        pass

    @abstractmethod
    def updateMessageToRead(self, message)->None:
        pass

    @abstractmethod
    def deleteMessage(self, message)->None:
        pass

    @abstractmethod
    def deleteDatabase(self)->None:
        pass

    @abstractmethod
    def _config(self, app:Flask)->None:
        pass


    @abstractmethod
    def _createMessagesTable(self):
        pass


    @abstractmethod
    def _createUsersTable(self):
        pass