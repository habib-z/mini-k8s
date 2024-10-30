from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict
from app.entity.user import User


class ChatRoom(ABC):

    users:List[User]
    message_user_seen:Dict[str, Dict[str, bool]]
    def seen(self,message:str,user_name:str):
        self.message_user_seen[message][user_name]=True
    def un_seen_num_for_user(self,user_name):
        num=0
        for (message,user) in self.message_user_seen.items():
            if(user_name==user):
                num+=self.message_user_seen[message][user_name]==False
        return num
    @property
    def messages(self)->List[str]:
        return list(self.message_user_seen.keys())


    def to_dict(self):
        chat_room={}
        chat_room['users']=[user.user_name for user in self.users]
        chat_room['messages']=self.messages
        chat_room['message_user_seen']=self.message_user_seen
        return chat_room
    def __eq__(self, other):
        return self.getId().__eq__(other.getId())
    @abstractmethod
    def getId(self)->str:
        return 'none'


