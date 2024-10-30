from app.entity.chat_room import ChatRoom
from app.entity.user import User


class PairChatRoom(ChatRoom):

    def __init__(self,u0:User,u1:User):
        self.users=[u0,u1]
        self.message_user_seen= {}


    def getId(self)->str:
        """Create Unique Identifier Based on Usernames"""
        u0:User=self.users[0]
        u1:User=self.users[1]
        if(u0.user_name<u1.user_name):
            t=u1
            u1=u0
            u0=t

        return f'{u1.user_name}&{u0.user_name}'
