from flask import Flask
from abc import ABC, abstractmethod
from datetime import date


#Database is an abstract class that represents a general interface for a database for this REST API
class Database(ABC):
    DATABASE_NAME:str = "Messaging_System.db"
    DATABASE_PATH:str = f"sqlite:///{DATABASE_NAME}"
    SECRET_KEY:str = "psjtk40gk5kf0orr9k3ns"


    @abstractmethod
    def insertNewMessage(self, id: int, senderUsername: str, receiverUsername: str, message: str, subject: str,creationDate: date, read: bool) -> None:
        pass


    @abstractmethod
    def insertNewUser(self, username: str, password: str, name: str) -> None:
        pass


    @abstractmethod
    def getAllMessages(self):
        pass


    @abstractmethod
    def getAllUsers(self, id:int, name:str):
        pass


    @abstractmethod
    def getMessage(self, id:int):
        pass

    @abstractmethod
    def getUser(self, username:str, password:str):
        pass

    @abstractmethod
    def deleteDatabase(self)->None:
        pass

    @abstractmethod
    def _config(self, app:Flask)->None:
        pass


    @abstractmethod
    def _createMessagesTable(self)->None:
        pass


    @abstractmethod
    def _createUsersTable(self)->None:
        pass