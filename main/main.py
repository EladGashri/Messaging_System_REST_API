from flask import Flask
from flask_restful import Api
from flask_injector import FlaskInjector
from injector import singleton
from security.jwt_utils import JwtUtils
from database.sql_alchemy_database import SqlAlchemyDatabase
from database.database import Database
from services.message_service import MessageService
from resources.authentication_resource import AuthenticationResource
from resources.messages_resource import MessagesResource
from resources.unread_messages_resource import UnreadMessagesResource
from resources.registration_resource import RegistrationResource
from services.user_service import UserService
from resources.resources_manager import ResourcesManager


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