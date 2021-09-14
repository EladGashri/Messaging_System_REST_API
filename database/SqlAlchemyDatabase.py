from database.Database import Database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import Optional


class SqlAlchemyDatabase(Database):

    def __init__(self, app:Flask, create:bool = True):
        self._config(app)
        self._db:SQLAlchemy = SQLAlchemy(app)
        self.MessagesClass=self._createMessagesTable()
        self.UserClass=self._createUsersTable()
        if create:
            self._db.create_all()


    def insertNewMessage(self, id: int, senderUsername: str, receiverUsername: str, message: str, subject: str,creationDate: date = date.today(), read: bool = False) -> None:
        newMessage = self.MessagesClass(id=id, senderUsername=senderUsername, receiverUsername=receiverUsername, message=message, subject=subject, creationDate=creationDate, read=read)
        self._db.session.add(newMessage)
        self._db.session.commit()


    def insertNewUser(self, username: str, password: str, name: str) -> None:
        newUser = self.UserClass(username=username, password=password, name=name)
        self._db.session.add(newUser)
        self._db.session.commit()


    def getAllMessages(self):
        return self.MessagesClass.query.all()


    def getAllUsers(self):
        return self.UserClass.query.all()


    def getMessage(self, id: int):
        return self.MessagesClass.query.filter_by(id=id).first()


    def getUser(self, username:str, password:str):
            return self.UserClass.query.filter_by(username=username, password=password).first()


    def deleteDatabase(self)->None:
        self._db.drop_all()


    def _config(self, app:Flask)->None:
        app.config["SQLALCHEMY_DATABASE_URI"] = Database.DATABASE_PATH
        app.config["SECRET_KEY"] = Database.SECRET_KEY
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    def _createMessagesTable(self) -> None:
        class Message(self._db.Model):
            id:int = self._db.Column(self._db.Integer, primary_key=True)
            senderUsername:int = self._db.Column(self._db.Integer, self._db.ForeignKey('user.username'), nullable=False)
            receiverUsername:int = self._db.Column(self._db.Integer, self._db.ForeignKey('user.username'), nullable=False)
            message:str = self._db.Column(self._db.String(500), unique=False, nullable=False)
            subject:str = self._db.Column(self._db.String(50), unique=False, nullable=False)
            creationDate:date = self._db.Column(self._db.Date, unique=False, nullable=False)
            read:bool = self._db.Column(self._db.Boolean, unique=False, nullable=False)
        return Message


    def _createUsersTable(self) -> None:
        Message=self.MessagesClass
        class User(self._db.Model):
            username: str = self._db.Column(self._db.String(50), primary_key=True)
            password: str = self._db.Column(self._db.String(50), nullable=False)
            name: str = self._db.Column(self._db.String(50), unique=False, nullable=False)
            messages = self._db.relationship("Message", foreign_keys=username, backref="sender", primaryjoin="User.username == Message.receiverUsername")
        return User