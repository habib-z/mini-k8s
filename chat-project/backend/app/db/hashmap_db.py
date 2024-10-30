import pickle
from os import unlink
from os.path import exists
from typing import List, Optional, Dict

from app.db.pickle_db_entity import DBList, DBDict
from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.entity.pair_chat_room import PairChatRoom
from app.entity.user import User
from app.repository.database import Database


class HashmapDB(Database):
    user_chat_rooms:DBDict[str, List[str]]
    pair_chats:DBDict[str,PairChatRoom]
    id_to_message:DBDict[str,Message]

    def __init__(self,path:str):
        self.path = path
        self.user_chat_rooms=DBDict(f'{self.path}/user_names.pkl')
        self.pair_chats=DBDict(f'{self.path}/pair_chat.pkl')
        self.id_to_message=DBDict(f'{self.path}/id_to_message.pkl')


    def get_chat_room_by_id(self, chat_room_id: str) -> ChatRoom:
        return self.pair_chats[chat_room_id]

    def get_message_by_id(self, msg_id:str)->Message:
        return self.id_to_message[msg_id]

    def create_user_name(self,user_name:str)->bool:
        if(user_name in self.user_chat_rooms):
            return False
        self.user_chat_rooms[user_name]=[]
        return True

    def get_user_by_name(self, user_name:str)->Optional[User]:
        if (user_name in self.user_chat_rooms.keys()):
            return User(user_name)

    def create_pair_chat(self, requesting_user: User, requested_user: User) -> PairChatRoom:
        created=PairChatRoom(requesting_user, requested_user)
        pairChatId=created.getId()
        if pairChatId in self.pair_chats.keys():
            return self.pair_chats[pairChatId]
        else:
            self.pair_chats[created.getId()]=created
            self.user_chat_rooms[requesting_user.user_name].append(pairChatId)
            self.user_chat_rooms[requested_user.user_name].append(pairChatId)
            return created

    def on_message_seen(self, user_name, message_id)->Message:
        message=self.id_to_message[message_id]
        chat_room=self.pair_chats[message.receiver.getId()]
        chat_room.seen(message_id,user_name)
        message.receiver=chat_room
        return message

    def send_message(self, message:Message):
        self.id_to_message[message.id]=message
        if message.receiver.getId() in self.pair_chats.keys():
            self.pair_chats[message.receiver.getId()].message_user_seen[message.id]={}
            receiver_id=message.receiver.getId()
            for user in self.pair_chats[receiver_id].users:
                self.pair_chats[receiver_id].message_user_seen[message.id][user.user_name]=False
            self.pair_chats[receiver_id].message_user_seen[message.id][message.sender.user_name]= True
            message.receiver=self.pair_chats[receiver_id]
            return True

    def get_user_chat_rooms(self, user: User)->List[ChatRoom]:
        return [self.pair_chats[chat_room_id] for chat_room_id in self.user_chat_rooms[user.user_name]]

    def __enter__(self):
        try:
            self.user_chat_rooms=self.user_chat_rooms.load()
            self.pair_chats=self.pair_chats.load()
            self.id_to_message=self.id_to_message.load()
        except (EOFError,FileNotFoundError) as e:
            print(f'error: {e}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.user_chat_rooms.save()
        self.pair_chats.save()
        self.id_to_message.save()

    def remove(self):
        self.user_chat_rooms.unlink()
        self.pair_chats.unlink()
        self.id_to_message.unlink()
