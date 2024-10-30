from abc import ABC
from typing import Optional, List

from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.entity.pair_chat_room import PairChatRoom
from app.entity.user import User


class Database(ABC):
    def create_user_name(self, user_name: str) -> bool:
        pass

    def get_user_by_name(self, user_name: str) -> Optional[User]:
        pass



    def create_pair_chat(self,requesting_user: User, requested_user: User) -> PairChatRoom:
        pass

    def get_user_chat_rooms(self,user:User)->List[ChatRoom]:
        pass
    def get_chat_room_by_id(self,chat_room_id:str)->ChatRoom:
        pass
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def send_message(self, message:Message):
        pass

    def on_message_seen(self, user_name, message_id)->Message:
        pass

    def get_message_by_id(self, msg_id:str)->Message:
        pass


    def remove(self)->None:
        pass





