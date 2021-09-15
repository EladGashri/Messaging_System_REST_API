from typing import Optional
from database.Database import Database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from entities.Message import Message
from entities.User import User


# SqlAlchemyDatabase is an implementation of the abstract class Database.
class SqlAlchemyDatabase(Database):

    def __init__(self, app:Flask, create:bool = True):
        self._config(app)
        self._db:SQLAlchemy = SQLAlchemy(app)
        self.message_class=self._create_message_table()
        self.user_class=self._create_user_table()
        if create:
            self._db.create_all()
        Message.last_message_id = self.get_number_of_messages()


    def insert_new_message(self, message:Message) -> None:
        date_str:str = message.creation_date.split("-")
        new_message = self.message_class(id=message.id, sender_username=message.sender_username, receiver_username=message.receiver_username,\
                                        message=message.message, subject=message.subject, creation_date=datetime(int(date_str[0]),int(date_str[1]),int(date_str[2])) , read=message.read)
        self._db.session.add(new_message)
        self._db.session.commit()


    def insert_new_user(self, user:User) -> None:
        new_user = self.user_class(username=user.username, password=user.password, name=user.name)
        self._db.session.add(new_user)
        self._db.session.commit()


    def get_number_of_messages(self) -> int:
        return len(self.message_class.query.all())


    def get_message(self, id: int, user=None, also_sender:bool = False):
        if user is not None:
            message = self.message_class.query.filter_by(id=id, receiver_username=user.username).first()
            if also_sender and message is None:
                message = self.message_class.query.filter_by(id=id, sender_username=user.username).first()
            return message
        else:
            return self.message_class.query.filter_by(id=id).first()


    def get_user(self, username:str, password:Optional[str] = None):
        if password is not None:
            return self.user_class.query.filter_by(username=username, password=password).first()
        else:
            return self.user_class.query.filter_by(username=username).first()


    def update_message_to_read(self, message) -> None:
        if isinstance(message, Message):
            message=self.getMessage(message.id)
        setattr(message, "read", True)
        self._db.session.commit()


    def delete_message(self, message) -> None:
        self.message_class.query.filter_by(id=message.id).delete()
        self._db.session.commit()


    def delete_database(self)->None:
        self._db.drop_all()


    def _config(self, app:Flask)->None:
        app.config["SQLALCHEMY_DATABASE_URI"] = Database.DATABASE_PATH
        app.config["SECRET_KEY"] = Database.SECRET_KEY
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    def _create_message_table(self):
        class Message(self._db.Model):
            id:int = self._db.Column(self._db.Integer, primary_key=True)
            sender_username:str = self._db.Column(self._db.String(50), self._db.ForeignKey('user.username'), unique=False, nullable=False)
            receiver_username:str = self._db.Column(self._db.String(50), self._db.ForeignKey('user.username'), unique=False, nullable=False)
            message:str = self._db.Column(self._db.String(500), unique=False, nullable=False)
            subject:str = self._db.Column(self._db.String(50), unique=False, nullable=False)
            creation_date:date = self._db.Column(self._db.Date, unique=False, nullable=False)
            read:bool = self._db.Column(self._db.Boolean, unique=False, nullable=False)
        return Message


    def _create_user_table(self) -> None:
        class User(self._db.Model):
            username: str = self._db.Column(self._db.String(50), primary_key=True)
            password: str = self._db.Column(self._db.String(50), nullable=False)
            name: str = self._db.Column(self._db.String(50), unique=False, nullable=False)
            sent_messages = self._db.relationship("Message", backref="sender", primaryjoin="User.username == Message.sender_username")
            received_messages = self._db.relationship("Message", backref="receiver", primaryjoin="User.username == Message.receiver_username")
        return User