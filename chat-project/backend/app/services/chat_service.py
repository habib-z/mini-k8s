from typing import List

from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.entity.pair_chat_room import PairChatRoom
from app.entity.user import User
from app.repository.chat_repository import ChatRepository
from app.repository.database import Database
from app.services.session_service import SessionService


class ChatService:

    @staticmethod
    def request_pair_chat(requesting_user:User,requested_user:User, database: Database) -> PairChatRoom:
        pair_chat_room= ChatRepository.request_pair_chat(requesting_user,requested_user, database)
        SessionService.new_chat_created(pair_chat_room)
        return pair_chat_room

    @staticmethod
    def send_message( message:Message,database: Database)->bool:
        result=ChatRepository.send_message(message,database)
        #if result:
        return result

    @staticmethod
    async def send_message_async(message: Message, database: Database) -> bool:
        result = ChatRepository.send_message(message, database)
        # if result:
        await SessionService.new_message_recieved(message)
        return result

    @staticmethod
    def get_chat_room_list(user:User, database:Database)->List[ChatRoom]:
        return ChatRepository.getChatRoomList(user,database)

    @staticmethod
    def get_chat_room_by_id( chat_room_id: str, database: Database) -> ChatRoom:
       return ChatRepository.get_chat_room_by_id(chat_room_id,database)

    @staticmethod
    def get_message_by_id(msg_id, database:Database):
        return ChatRepository.getMessageById(msg_id,database)