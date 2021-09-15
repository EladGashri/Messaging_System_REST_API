from entities.Message import Message
from database.Database import Database
from typing import List, Dict, Optional


# The MessageService class contains the buisness logic related to the message table in the database
class MessageService:


    def getMessage(self, messageId:int, user, database:Database) -> Optional[Dict[str,str]]:
        message = database.getMessage(messageId, user)
        if message is not None:
            messageAsDict = Message.getMessagefromModel(message).getMessageAsDict()
            database.updateMessageToRead(message)
            return messageAsDict
        else:
            return None


    def getUserMessages(self, user, database:Database, onlyUnreadMessages :bool = False) -> List[Dict[str,str]]:
        if onlyUnreadMessages:
            messages=[message for message in user.receivedMessages if not message.read]
        else:
            messages=user.receivedMessages
        messagesAsDicts = [Message.getMessagefromModel(message).getMessageAsDict() for message in messages]
        for message in messages:
            if not message.read:
                database.updateMessageToRead(message)
        return messagesAsDicts



    def insertMessage(self, senderUsername:str, receiverUsername:str, subject:str, message:str, database:Database) -> int:
        Message.incrementLastMessageId()
        message:Message = Message(Message.lastMessageId, senderUsername, receiverUsername, subject, message)
        database.insertNewMessage(message)
        return message.id


    def deleteMessage(self, messageId:int, user, database:Database) -> bool:
        message = database.getMessage(messageId, user, alsoSender=True)
        if message is not None:
            database.deleteMessage(message)
            return True
        else:
            return False