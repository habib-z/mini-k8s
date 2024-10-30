from dataclasses import dataclass
from typing import AnyStr


class MessageContent:
    pass

@dataclass
class TextMessage(MessageContent):
    text:str

@dataclass
class AudioMessage(MessageContent):
    content:AnyStr