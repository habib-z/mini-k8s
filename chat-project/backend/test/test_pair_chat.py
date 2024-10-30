from datetime import datetime
from typing import List
from unittest import TestCase

from app.db import create_default_db
from app.entity.chat_room import ChatRoom
from app.entity.message import Message
from app.entity.message_content import TextMessage
from app.entity.pair_chat_room import PairChatRoom
from app.services.chat_service import ChatService
from app.services.user_service import UserService


class TestPairChat(TestCase):

    def setUp(self) -> None:
        self.database = create_default_db()
        self.database.remove()
        self.database = create_default_db()
        self.sara = UserService.create_user("sara", self.database)
        self.ali = UserService.create_user("ali", self.database)

    def tearDown(self) -> None:
        ...

    def test_create_pair_chat(self) -> None:
        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        self.assertIsInstance(pair_chat, PairChatRoom)

    def test_send_message_to_pair_confirm(self) -> None:
        sample_text="salam"
        pair_chat = ChatService.request_pair_chat(self.sara, self.ali, self.database)
        message = Message(self.sara, pair_chat, TextMessage(sample_text), datetime.now())
        result = ChatService.send_message(message,self.database)
        self.assertTrue(result)
        chatList:List[ChatRoom]=ChatService.get_chat_room_list(self.ali, self.database)
        self.assertEqual(len(chatList),1)
        self.assertIsInstance(chatList[0],PairChatRoom)
        self.assertEqual(chatList[0].getId(), pair_chat.getId())
        self.assertEqual(chatList[0], pair_chat)
        self.assertEqual(len(chatList[0].messages),1)
        msg00_id=chatList[0].messages[0]
        message=ChatService.get_message_by_id(msg00_id, self.database)
        self.assertIsInstance(message.content,TextMessage)
        self.assertEqual(message.content.text,sample_text)


