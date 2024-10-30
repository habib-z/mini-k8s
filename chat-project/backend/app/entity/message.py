from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


from app.entity.message_content import MessageContent
from app.entity.user import User


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.entity.chat_room import ChatRoom
@dataclass
class Message:
    sender:User
    receiver:ChatRoom
    content: MessageContent
    date_time:datetime

    @property
    def id(self):
        return f"{self.sender.user_name}@{self.receiver.getId()}@{self.date_time.strftime('%Y-%m-%d %H:%M:%S.%f')}"

    def to_dict(self):
        message={}
        message['sender']=self.sender.user_name
        message['reciever']=self.receiver.getId()
        message['content']=self.content.__dict__
        message['date_time']=self.date_time.__str__()
        return message


