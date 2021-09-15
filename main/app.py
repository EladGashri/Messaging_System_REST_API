from flask import Flask
from flask_restful import Api
from flask_injector import FlaskInjector
from injector import singleton
from security.JwtUtils import JwtUtils
from database.SqlAlchemyDatabase import SqlAlchemyDatabase
from database.Database import Database
from services.MessageService import MessageService
from resources.AuthenticationResource import AuthenticationResource
from resources.MessagesResource import MessagesResource
from resources.UnreadMessagesResource import UnreadMessagesResource
from resources.RegistrationResource import RegistrationResource
from services.UserService import UserService
from resources.ResourcesManager import ResourcesManager


app: Flask = Flask(__name__)
api: Api = Api(app)


# By using dependency injection for the Database class I am implementing the dependency inversion principle in SOLID.
# This occures because the application is not dependent on the Database implementation (SqlAlchemyDatabase), it is only dependent on the abstract class (Database).
def configure(binder):
    binder.bind(Database, to=SqlAlchemyDatabase(app), scope=singleton)
    binder.bind(JwtUtils, to=JwtUtils(app), scope=singleton)
    binder.bind(MessageService, to=MessageService(), scope=singleton)
    binder.bind(UserService, to=UserService(), scope=singleton)
    binder.bind(ResourcesManager, to=ResourcesManager(), scope=singleton)


api.add_resource(MessagesResource, "/messaging-system/messages")
api.add_resource(UnreadMessagesResource, "/messaging-system/messages/unread")
api.add_resource(AuthenticationResource, "/messaging-system/authentication")
api.add_resource(RegistrationResource, "/messaging-system/registration")


if __name__ == "__main__":
    FlaskInjector(app=app, modules=[configure])
    app.run()