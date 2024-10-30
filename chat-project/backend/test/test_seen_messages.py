from datetime import datetime
from unittest import TestCase

from app.db import create_default_db
from app.entity.message import Message
from app.entity.message_content import TextMessage
from app.services.chat_service import ChatService
from app.services.session_service import SessionService
from app.services.user_service import UserService


class TestSeenMessage(TestCase):

    def setUp(self) -> None:
        self.database = create_default_db()
        self.database.remove()
        self.database = create_default_db()
        self.sara = UserService.create_user("sara", self.database)
        self.ali = UserService.create_user("ali", self.database)
        self.hassan = UserService.create_user("hassan", self.database)

    def tearDown(self) -> None:
        ...

    def test_when_message_generated_it_first_seen_only_by_the_sender(self):
        sample_text1 = "salam"
        sample_text2 = "chetori"

        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        message = Message(self.sara, pair_chat, TextMessage(sample_text1), datetime.now())
        result = ChatService.send_message(message, self.database)

        chat_room=ChatService.request_pair_chat(self.sara,self.ali,self.database)
        self.assertIsNotNone(chat_room.message_user_seen.get(message.id))
        self.assertIsNotNone(chat_room.message_user_seen.get(message.id).get(self.sara.user_name))
        self.assertTrue(chat_room.message_user_seen.get(message.id)[self.sara.user_name])
        self.assertFalse(chat_room.message_user_seen.get(message.id)[self.ali.user_name])

    def sendMessage(self,message,ali2sara=True):
        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        message = Message(self.ali if ali2sara else self.sara, pair_chat, TextMessage(message), datetime.now())
        return ChatService.send_message(message, self.database)

    def test_when_message_generated_it_first_seen_only_by_the_sender_and_false_by_other_active_user(self):
        sample_text1 = "salam"
        sample_text2 = "chetori"
        SessionService.login_user(self.ali.user_name, self.database)
        ali_view_model = SessionService.get_user_session(self.ali.user_name)
        self.assertEqual(len(ali_view_model.chat_rooms), 0)
        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms), 1)
        message = Message(self.sara, pair_chat, TextMessage(sample_text1), datetime.now())
        result = ChatService.send_message(message, self.database)
        chat_room_key = list(ali_view_model.chat_rooms.keys())[0]
        chat_room=ali_view_model.chat_rooms[chat_room_key]
        self.assertIsNotNone(chat_room.message_user_seen.get(message.id))
        self.assertIsNotNone(chat_room.message_user_seen.get(message.id).get(self.sara.user_name))
        self.assertTrue(chat_room.message_user_seen.get(message.id)[self.sara.user_name])
        self.assertFalse(chat_room.message_user_seen.get(message.id)[self.ali.user_name])

    def test_when_message_seen_by_other_it_will_be_saved(self):
        sample_text1 = "salam"
        sample_text2 = "chetori"
        SessionService.login_user(self.ali.user_name, self.database)
        ali_view_model = SessionService.get_user_session(self.ali.user_name)
        self.assertEqual(len(ali_view_model.chat_rooms), 0)

        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        self.assertEqual(len(ali_view_model.chat_rooms), 1)
        message = Message(self.sara, pair_chat, TextMessage(sample_text1), datetime.now())
        result = ChatService.send_message(message, self.database)
        chat_room_key = list(ali_view_model.chat_rooms.keys())[0]
        chat_room=ali_view_model.chat_rooms[chat_room_key]
        self.assertEqual(len(chat_room.messages),1)
        SessionService.message_seen(self.ali.user_name,chat_room.messages[0],self.database)
        self.assertTrue(chat_room.message_user_seen.get(message.id)[self.ali.user_name])
        chat_room = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        self.assertIsNotNone(chat_room.message_user_seen.get(message.id))
        self.assertIsNotNone(chat_room.message_user_seen.get(message.id).get(self.sara.user_name))
        self.assertTrue(chat_room.message_user_seen.get(message.id)[self.sara.user_name])
        self.assertTrue(chat_room.message_user_seen.get(message.id)[self.ali.user_name])

        key=list(ali_view_model.chat_rooms.keys())[0]
        self.assertTrue(ali_view_model.chat_rooms[key].message_user_seen[message.id][self.ali.user_name])
        self.assertTrue(ali_view_model.chat_rooms[key].message_user_seen[message.id][self.sara.user_name])

        SessionService.login_user(self.sara.user_name, self.database)
        sara_view_model = SessionService.get_user_session(self.sara.user_name)
        key=list(sara_view_model.chat_rooms.keys())[0]
        self.assertTrue(sara_view_model.chat_rooms[key].message_user_seen[message.id][self.ali.user_name])
        self.assertTrue(sara_view_model.chat_rooms[key].message_user_seen[message.id][self.sara.user_name])