from typing import List

from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.entity.pair_chat_room import PairChatRoom
from app.entity.user import User
from app.repository.database import Database


class ChatRepository:

    @staticmethod
    def request_pair_chat(requesting_user: User, requested_user: User, database: Database) -> PairChatRoom:
        with database:
            pair_chat_room = database.create_pair_chat(requesting_user,requested_user)
            return pair_chat_room

    @staticmethod
    def send_message( message:Message,database: Database)->bool:
        with database:
            result= database.send_message(message)
        return result

    @staticmethod
    def getChatRoomList(user: User, database: Database)->List[ChatRoom]:
        with database:
            return database.get_user_chat_rooms(user)
    @staticmethod
    def get_chat_room_by_id(chat_room_id:str,database:Database)->ChatRoom:
         with database:
             return database.get_chat_room_by_id(chat_room_id)
    @staticmethod
    def message_seen(user_name:str,message_id:str,database:Database)->Message:
        with database:
            result = database.on_message_seen(user_name, message_id)
            return result

    @staticmethod
    def getMessageById(msg_id:str, database:Database)->Message:
        with database:
            return database.get_message_by_id(msg_id)