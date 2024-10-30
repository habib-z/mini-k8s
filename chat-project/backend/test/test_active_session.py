from datetime import datetime
from typing import List
from unittest import TestCase

from app.db import create_default_db
from app.db.redis_db import RedisDB
from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.entity.message_content import TextMessage
from app.entity.pair_chat_room import PairChatRoom
from app.services.chat_service import ChatService
from app.services.session_service import SessionService
from app.services.user_service import UserService


class TestActiveSession(TestCase):

    def setUp(self) -> None:
        self.database = create_default_db()
        self.database.remove()
        self.database = create_default_db()
        self.sara = UserService.create_user("sara", self.database)
        self.ali = UserService.create_user("ali", self.database)

    def tearDown(self) -> None:
        ...


    def test_login_user(self)->None:
        SessionService.login_user(self.ali.user_name, self.database)

    def test_user_view_model_should_find_chat_created_when_login(self)->None:
        sample_text = "salam"
        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        message = Message(self.sara, pair_chat, TextMessage(sample_text), datetime.now())
        result = ChatService.send_message(message, self.database)
        ali_view_model = SessionService.login_user(self.ali.user_name, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms.keys()), 1)
        chat_room_key=list(ali_view_model.chat_rooms.keys())[0]
        self.assertEqual(ali_view_model.chat_rooms[chat_room_key], pair_chat)
        self.assertEqual(len(ali_view_model.chat_rooms[chat_room_key].messages), 1)

    def test_user_view_model_update_when_receive_new_messages_for_first_time(self) -> None:
        SessionService.login_user(self.ali.user_name,self.database)
        ali_view_model = SessionService.get_user_session(self.ali.user_name)
        self.assertEqual(len(ali_view_model.chat_rooms), 0)
        sample_text = "salam"
        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms), 1)
        message = Message(self.sara, pair_chat, TextMessage(sample_text), datetime.now())
        chat_room_key = list(ali_view_model.chat_rooms.keys())[0]
        self.assertEqual(len(ali_view_model.chat_rooms[chat_room_key].messages), 0)
        result = ChatService.send_message(message, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms[chat_room_key].messages), 1)
        self.assertEqual(len(ali_view_model.chat_rooms), 1)
        self.assertEqual(ali_view_model.chat_rooms[chat_room_key], pair_chat)
        self.assertEqual(len(ali_view_model.chat_rooms[chat_room_key].messages), 1)


    def test_user_view_model_update_when_receive_new_messages_from_already_exist_chat(self) -> None:
        sample_text1 = "salam"
        sample_text2 = "chetori"
        SessionService.login_user(self.ali.user_name,self.database)
        ali_view_model = SessionService.get_user_session(self.ali.user_name)
        self.assertEqual(len(ali_view_model.chat_rooms), 0)

        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms), 1)
        message = Message(self.sara, pair_chat, TextMessage(sample_text1), datetime.now())
        result = ChatService.send_message(message, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms.keys()), 1)
        chat_room_key = list(ali_view_model.chat_rooms.keys())[0]
        self.assertEqual(ali_view_model.chat_rooms[chat_room_key], pair_chat)
        self.assertEqual(len(ali_view_model.chat_rooms[chat_room_key].messages), 1)
        message = Message(self.sara, pair_chat, TextMessage(sample_text2), datetime.now())
        result = ChatService.send_message(message, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms[chat_room_key].messages), 2)


