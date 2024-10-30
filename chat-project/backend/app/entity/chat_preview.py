from app.entity.chat_room import ChatRoom


class ChatPreview:
    chat_name:str
    chat_room_id:str
    num_of_unseen:int
    last_message_id:str
    pic_url:str

    def __init__(self,user_name,chat_room:ChatRoom):
        self.chat_name= chat_room.getId()
        self.chat_room_id= chat_room.getId()
        self.num_of_unseen= chat_room.un_seen_num_for_user(user_name)
        self.last_message_id= chat_room.messages[-1] if len(chat_room.messages) > 0 else None
        self.pic_url= ""

    def to_dict(self) -> dict:
        chat_preview = {}
        chat_preview['chat_name'] = self.chat_name
        chat_preview['chat_room_id'] = self.chat_room_id
        chat_preview['num_of_unseen'] = self.num_of_unseen
        if (self.last_message_id is not None):
            chat_preview['last_message_id'] = self.last_message_id
        chat_preview['pic_url'] = self.pic_url
        return chat_preview