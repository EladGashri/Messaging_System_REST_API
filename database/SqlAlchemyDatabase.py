from database.Database import Database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from typing import Dict, Optional


class SqlAlchemyDatabase(Database):

    def __init__(self, app:Flask):
        self._createDatabase(app)
        self._db:SQLAlchemy = SQLAlchemy(app)
        self.MessagesClass=self._createMessagesTable()
        self.UserClass=self._createUsersTable()
        self._db.create_all()


    def insertNewMessage(self, id: int, senderId: int, receiverId: int, message: str, subject: str,creationDate: date = date.today(), read: bool = False) -> None:
        newMessage = self.MessagesClass(id, senderId, receiverId, message, subject, creationDate, read)
        self._db.session.add(newMessage)
        self._db.session.commit()


    def insertNewUser(self, username: str, password: str, name: str) -> None:
        print("trying to insert "+username)
        newUser = self.UserClass(username=username, password=password, name=name)
        self._db.session.add(newUser)
        self._db.session.commit()
        print(username+" inserted")


    def getAllMessages(self):
        return self.MessagesClass.query.all()


    def getAllUsers(self):
        return self.UserClass.query.all()


    def getMessage(self, id: int):
        return self.MessagesClass.query.filter_by(id=id).first()


    def getUser(self, username: str = None, password:str = None):
        if username is None and password is None:
            return None
        elif password is None:
            return self.UserClass.query.filter_by(username=username).first()
        else:
            return self.UserClass.query.filter_by(username=username, password=password).first()


    def getUserFromUserFeilds(self, userFields:Dict[str,str]):
        username:Optional[str] = userFields.get("username",None)
        password:Optional[str] = userFields.get("password",None)
        return self.getUser(username,password)


    def deleteDatabase(self)->None:
        self._db.drop_all()


    def _createDatabase(self, app:Flask)->None:
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
            messages = self._db.relationship("Message", foreign_keys=username, backref="sender", primaryjoin="User.username == Message.senderUsername")
        return User