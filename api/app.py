from flask import Flask
from flask_restful import Api
from flask_injector import FlaskInjector
from injector import singleton
from security.JwtUtils import JwtUtils
from database.SqlAlchemyDatabase import SqlAlchemyDatabase
from database.Database import Database
from resources.AuthenticationResource import AuthenticationResource
from resources.MessagesResource import MessagesResource
from resources.UnreadMessagesResource import UnreadMessagesResource


app: Flask = Flask(__name__)
api: Api = Api(app)


#By using dependency injection for the Database and JWT classes we are implementing the dependency inversion principle in SOLID
#This occures because the application is not dependent on the Database implementation (SqlAlchemyDatabase), it is only dependent on the abstract class (Database)
def configure(binder):
    binder.bind(JwtUtils, to=JwtUtils(app), scope=singleton)
    binder.bind(Database, to=SqlAlchemyDatabase(app), scope=singleton)


api.add_resource(MessagesResource, "/messaging-system/messages")
api.add_resource(UnreadMessagesResource, "/messaging-system/messages/unread")
api.add_resource(AuthenticationResource, "/messaging-system/authentication")


if __name__ == "__main__":
    FlaskInjector(app=app, modules=[configure])
    app.run(debug=True)