from typing import Dict, List

from app.entity.chat_preview import ChatPreview
from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.model_view.user_main_view_model import UserMainModelView
from app.repository.chat_repository import ChatRepository
from app.repository.database import Database
from app.repository.user_repository import UserRepository
from app.services.connection_manager import ConnectionManager


class SessionService:

    active_session:Dict[str,UserMainModelView]={}
    @classmethod
    def login_user(cls,user_name:str, database: Database) -> List[ChatPreview]:
        user=UserRepository.find_user(user_name,database)
        chat_room_list=ChatRepository.getChatRoomList(user,database)
        print(f"chat room list for user {user_name} is {chat_room_list}")
        chat_rooms={chat_room.getId():chat_room for chat_room in chat_room_list}
        userViewModel=UserMainModelView(user,chat_rooms)
        cls.active_session[user_name]=userViewModel
        chat_preview_list = [ChatPreview(user_name, chat_room).to_dict() for chat_room in chat_room_list]
        return chat_preview_list

    @classmethod
    def logout_uesr(cls,user_name:str, database: Database)->None:
        del cls.active_session[user_name]

    @classmethod
    def is_logged_in(cls, user_name:str):
        return user_name in cls.active_session.keys()

    @classmethod
    def get_user_session(cls,user_name:str)->UserMainModelView:
        return cls.active_session.get(user_name)

    @classmethod
    def new_chat_created(cls, chat_room:ChatRoom):
        for user in chat_room.users:
            if (user.user_name in cls.active_session):
                cls.active_session[user.user_name].chat_rooms[chat_room.getId()]=chat_room

    @classmethod
    async def new_message_recieved(cls, message:Message):
        chat_room=message.receiver
        # for user in chat_room.users:
        #     if user.user_name in cls.active_session.keys():
        #         if chat_room.getId() not in cls.active_session[user.user_name].chat_rooms.keys():
        #             cls.active_session[user.user_name].chat_rooms[chat_room.getId()]=chat_room
        #         else:
        #             for cr in cls.active_session[user.user_name].chat_rooms:
        #                 if cr.__eq__(chat_room):
        #                     cls.active_session[user.user_name].chat_rooms[chat_room.getId()]=chat_room
        await ConnectionManager.sendMessage(message)



    @classmethod
    def message_seen(cls,user_name:str,message_id:str,database:Database):
        message=ChatRepository.message_seen(user_name,message_id,database)
        for user in message.receiver.users:
            if user.user_name in cls.active_session.keys():
                    cls.active_session[user.user_name].chat_rooms[message.receiver.getId()]\
                                    .message_user_seen[message_id][user_name]=True