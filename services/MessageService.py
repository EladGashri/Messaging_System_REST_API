from entities.Message import Message
from database.Database import Database
from typing import List, Dict, Optional


# The MessageService class contains the buisness logic related to the message table in the database
class MessageService:


    def get_message(self, message_id:int, user, database:Database) -> Optional[Dict[str,str]]:
        message = database.get_message(message_id, user)
        if message is not None:
            message_as_dict = Message.get_message_from_model(message).as_dict()
            database.update_message_to_read(message)
            return message_as_dict
        else:
            return None


    def get_user_messages(self, user, database:Database, only_unread_messages :bool = False) -> List[Dict[str,str]]:
        if only_unread_messages:
            messages=[message for message in user.received_messages if not message.read]
        else:
            messages=user.received_messages
        messages_as_dicts = [Message.get_message_from_model(message).as_dict() for message in messages]
        for message in messages:
            if not message.read:
                database.update_message_to_read(message)
        return messages_as_dicts


    def insert_message(self, sender_username:str, receiver_username:str, subject:str, message:str, database:Database) -> int:
        Message.increment_last_message_id()
        message:Message = Message(Message.last_message_id, sender_username, receiver_username, subject, message)
        database.insert_new_message(message)
        return message.id


    def delete_message(self, message_id:int, user, database:Database) -> bool:
        message = database.get_message(message_id, user, also_sender=True)
        if message is not None:
            database.delete_message(message)
            return True
        else:
            return False