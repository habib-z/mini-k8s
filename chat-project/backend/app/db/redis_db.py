import pickle
from os import unlink
from typing import List, Optional

import redis

from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.entity.pair_chat_room import PairChatRoom
from app.entity.user import User
from app.repository.database import Database


class RedisDB(Database):



    def __init__(self):
        self.redis_db = redis.Redis(host='database', port=6379, decode_responses=False)

    def get_message_by_id(self, msg_id:str)->Message:
        j=self.redis_db.get(f"message:{msg_id}")
        return pickle.loads(j)

    def set_message_by_id(self, message:Message)->bool:
        return self.redis_db.set(f"message:{message.id}",pickle.dumps(message))

    def get_chat_room_by_id(self, chat_room_id: str) -> ChatRoom:
        j = self.redis_db.get(f"chat_room:{chat_room_id}")
        if j is not None:
            return pickle.loads(j)
        return None

    def set_chat_room_by_id(self, chat_room: ChatRoom) -> bool:
        return self.redis_db.set(f"chat_room:{chat_room.getId()}", pickle.dumps(chat_room))


    def create_user_name(self,user_name:str)->bool:
        old_user_name=self.redis_db.get(f'user_name:{user_name}')
        if(old_user_name is None):
            self.redis_db.set(f'user_name:{user_name}',user_name)
            return True
        return False


    def get_user_by_name(self, user_name:str)->Optional[User]:
        user = self.redis_db.get(f'user_name:{user_name}')
        if user:
            return User(user_name)

    def insert_new_chat(self, user_name:str, chat_room_id:str):
        self.redis_db.lpush(f'chat:{user_name}',chat_room_id)

    def create_pair_chat(self, requesting_user: User, requested_user: User) -> PairChatRoom:
        created=PairChatRoom(requesting_user, requested_user)
        pairChatId=created.getId()
        chat_room=self.get_chat_room_by_id(pairChatId)
        if chat_room is not None:
            return chat_room
        else:
            print('create new chat room: '+pairChatId)
            self.set_chat_room_by_id(created)
            self.insert_new_chat(requesting_user.user_name, pairChatId)
            self.insert_new_chat(requested_user.user_name, pairChatId)
            return created

    def on_message_seen(self, user_name, message_id)->Message:
        message=self.get_message_by_id(message_id)
        chat_room=self.get_chat_room_by_id(message.receiver.getId())
        chat_room.seen(message_id,user_name)
        message.receiver=chat_room
        self.set_chat_room_by_id(chat_room)
        return message

    def send_message(self, message:Message):
        self.set_message_by_id(message)
        chat_room=self.get_chat_room_by_id(message.receiver.getId())
        print(f'get chatroom by id id is: {chat_room.getId()}')
        if  chat_room:
            chat_room.message_user_seen[message.id]={}
            receiver_id=message.receiver.getId()
            for user in chat_room.users:
                chat_room.message_user_seen[message.id][user.user_name]=False
            chat_room.message_user_seen[message.id][message.sender.user_name]= True
            message.receiver=chat_room
            self.set_chat_room_by_id(chat_room)
            print(f'get chatroom by id id is: {message.receiver.getId()}')
            return True

    def get_user_chat_rooms(self, user: User)->List[ChatRoom]:
        chat_room_ids= self.redis_db.lrange(f'chat:{user.user_name}',0,-1)
        return [self.get_chat_room_by_id(id.decode()) for id in chat_room_ids]


    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def remove(self):
        self.redis_db.flushdb()
