from dataclasses import dataclass
from typing import List

from app.entity.chat_room import ChatRoom
from app.entity.user import User

@dataclass
class UserMainModelView:
    user: User
    chat_rooms: dict[str,ChatRoom]
