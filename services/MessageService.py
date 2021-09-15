from entities.Message import Message
from typing import List, Dict, Optional

class MessageService:


    def getMessage(messageId:int, user, database):
        message = database.getMessage(messageId, user)
        if message is not None:
            messageAsDict = Message.getMessagefromModel(message).getMessageAsDict()
            database.updateMessageToRead(message)
            return messageAsDict
        else:
            return None


    def getUserMessages(user, database, onlyUnreadMessages :bool = False) -> Optional[List[Dict[str,str]]]:
        if onlyUnreadMessages:
            messages=[message for message in user.receivedMessages if not message.read]
        else:
            messages=user.receivedMessages
        messagesAsDicts = [Message.getMessagefromModel(message).getMessageAsDict() for message in messages]
        for message in messages:
            if not message.read:
                database.updateMessageToRead(message)
        return messagesAsDicts



    def insertMessage(senderUserName:str, receiverUsername:str, subject:str, message:str, database) -> int:
        cls._incrementNumberOfMesages()
        message:Message = cls(cls.numberOfMessages, senderUserName, receiverUsername, subject, message)
        database.insertNewMessage(message)
        return message.id


    def deleteMessage(messageId:int, user, database) -> bool:
        message = database.getMessage(messageId, user, alsoSender=True)
        if message is not None:
            database.deleteMessage(message)
            return True
        else:
            return False