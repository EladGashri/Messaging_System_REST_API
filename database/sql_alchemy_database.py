from typing import Optional
from sqlalchemy import func
from database.database import Database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from entities.message import Message
from entities.user import User


# SqlAlchemyDatabase is an implementation of the abstract class Database.
class SqlAlchemyDatabase(Database):

    def __init__(self, app:Flask, create:bool = True):
        self._config(app)
        self._sql_alchemy:SQLAlchemy = SQLAlchemy(app)
        self._message_class=self._create_message_table()
        self._user_class=self._create_user_table()
        if create:
            self._sql_alchemy.create_all()
        self._set_last_message_id()


    def insert_new_message(self, message:Message) -> None:
        date_str:str = message.creation_date.split("-")
        new_message = self._message_class(id=message.id, sender_username=message.sender_username, receiver_username=message.receiver_username, \
                                          message=message.message, subject=message.subject, creation_date=datetime(int(date_str[0]),int(date_str[1]),int(date_str[2])), read=message.read)
        self._sql_alchemy.session.add(new_message)
        self._sql_alchemy.session.commit()


    def insert_new_user(self, user:User) -> None:
        new_user = self._user_class(username=user.username, password=user.password, name=user.name)
        self._sql_alchemy.session.add(new_user)
        self._sql_alchemy.session.commit()


    def get_message(self, id: int, user=None, also_sender:bool = False):
        if user is not None:
            message = self._message_class.query.filter_by(id=id, receiver_username=user.username).first()
            if also_sender and message is None:
                message = self._message_class.query.filter_by(id=id, sender_username=user.username).first()
            return message
        else:
            return self._message_class.query.filter_by(id=id).first()


    def get_user(self, username:str, password:Optional[str] = None):
        if password is not None:
            return self._user_class.query.filter_by(username=username, password=password).first()
        else:
            return self._user_class.query.filter_by(username=username).first()


    def update_message_to_read(self, message) -> None:
        if isinstance(message, Message):
            message=self.getMessage(message.id)
        setattr(message, "read", True)
        self._sql_alchemy.session.commit()


    def delete_message(self, message) -> None:
        self._message_class.query.filter_by(id=message.id).delete()
        self._sql_alchemy.session.commit()


    def delete_database(self)->None:
        self._sql_alchemy.drop_all()


    def _config(self, app:Flask)->None:
        app.config["SQLALCHEMY_DATABASE_URI"] = Database.DATABASE_PATH
        app.config["SECRET_KEY"] = Database.SECRET_KEY
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    def _create_message_table(self):
        class Message(self._sql_alchemy.Model):
            id:int = self._sql_alchemy.Column(self._sql_alchemy.Integer, primary_key=True)
            sender_username:str = self._sql_alchemy.Column(self._sql_alchemy.String(50), self._sql_alchemy.ForeignKey('user.username'), unique=False, nullable=False)
            receiver_username:str = self._sql_alchemy.Column(self._sql_alchemy.String(50), self._sql_alchemy.ForeignKey('user.username'), unique=False, nullable=False)
            message:str = self._sql_alchemy.Column(self._sql_alchemy.String(500), unique=False, nullable=False)
            subject:str = self._sql_alchemy.Column(self._sql_alchemy.String(50), unique=False, nullable=False)
            creation_date:date = self._sql_alchemy.Column(self._sql_alchemy.Date, unique=False, nullable=False)
            read:bool = self._sql_alchemy.Column(self._sql_alchemy.Boolean, unique=False, nullable=False)
        return Message


    def _create_user_table(self) -> None:
        class User(self._sql_alchemy.Model):
            username: str = self._sql_alchemy.Column(self._sql_alchemy.String(50), primary_key=True)
            password: str = self._sql_alchemy.Column(self._sql_alchemy.String(50), nullable=False)
            name: str = self._sql_alchemy.Column(self._sql_alchemy.String(50), unique=False, nullable=False)
            sent_messages = self._sql_alchemy.relationship("Message", backref="sender", primaryjoin="User.username == Message.sender_username")
            received_messages = self._sql_alchemy.relationship("Message", backref="receiver", primaryjoin="User.username == Message.receiver_username")
        return User


    def _set_last_message_id(self) -> None:
        if self._sql_alchemy.session.query(self._message_class).first() is None:
            Message.last_message_id=0
        else:
            Message.last_message_id = self._sql_alchemy.session.query(func.max(self._message_class.id)).scalar()