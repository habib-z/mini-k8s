import json
import pickle
from datetime import datetime

import redis



if __name__ == '__main__':
    from app.entity.message import Message
    from app.entity.message_content import TextMessage
    from app.entity.pair_chat_room import PairChatRoom
    from app.entity.user import User

    r = redis.Redis(host='localhost', port=6379, decode_responses=False)

    m:Message
    u1=User("1")
    u2=User("1")
    chatroom=PairChatRoom(u1,u2)
    m=Message(u1,chatroom,TextMessage("salam"),datetime.now())

    mobj=pickle.dumps(m)

    r.set("m1",mobj)


    n=pickle.loads(r.get("m1"))

