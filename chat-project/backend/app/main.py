import datetime
import logging
from dataclasses import dataclass

from fastapi import FastAPI, Form, UploadFile
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.entity.message import Message
from app.entity.message_content import TextMessage, AudioMessage
from app.entity.user import User
from app.services.chat_service import ChatService
from app.services.connection_manager import ConnectionManager
from app.services.session_service import SessionService
from app.services.user_service import UserService
from test.test_seen_messages import TestSeenMessage
from pydantic import BaseModel

# uvicorn app.main:app --reload --port 8000
# Function abr {kubectl --kubeconfig 'C:\Users\Habib\.kube\ir-thr-ba2-chatconfig.config'}



t=TestSeenMessage()
t.setUp()
#t.test_when_message_generated_it_first_seen_only_by_the_sender_and_false_by_other_active_user()
t.sendMessage('salam',True)
t.sendMessage('salam,chetori',False)
t.sendMessage('خوبم. تو چطوری؟',True)
t.sendMessage('manam khubam maslan, kheili matne bozorgie in\n matni ke daram say mikonam bozorgtar az hadde mamool benevisamesh' ,False)
t.sendMessage('dige che khabar' ,False)
db=t.database

pair_chat = ChatService.request_pair_chat(t.hassan, t.ali, t.database)
message = Message(t.ali, pair_chat, TextMessage("چطوری حسن"), datetime.datetime.now())
ChatService.send_message(message, db)

# file_location = f"{audio_file.filename}"
# with open(file_location, "wb+") as file_object:
#     file_object.write(user.file.read())

from pathlib import Path
contents = Path('name1').read_text()

message = Message(t.ali, pair_chat,
                  AudioMessage(content=contents), datetime.datetime.now())
ChatService.send_message(message, db)





app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5174",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:8888",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.getLogger('fastapi').setLevel(logging.DEBUG)
@dataclass
class SignUpDataRes:
    result:bool
@dataclass
class SignUpData:
    user_name:str
@dataclass
class ChatData:
    chat_id:str

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request,exc:RequestValidationError):
#     logging.error(f'request validation error:{exc}')
#     return {'detail': str(exc)}

class Data(BaseModel):
    user: str
@app.post("/fileupload")
async def uploadfile(user: UploadFile = Form(...)):
    print("recive data ...")
    file_location = f"{user.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(user.file.read())

    return {"message": "recieved"}

@app.get("/get_audio1/")
async def get_audio():
    from starlette.responses import FileResponse
    print('request_audio')
    return FileResponse('name1', media_type='audio/webm', filename='name1')


# @app.post("/fileupload")
# async def uploadfile(data: Data):
#     print("recive data ...")
#     print(data)
#     return {"message": "recieved"}

@app.post("/signup")
async def sign_up(signUpData:SignUpData):
    print(f"posted: {signUpData}")
    return SignUpDataRes(result=True)

@app.post("/login/{user_name}")
async def login(user_name:str):
    print(f"posted: {user_name}")
    user=UserService.find_user(user_name,database=db)
    if not user:
        UserService.create_user(user_name,database=db)
    chat_preview_list=SessionService.login_user(user_name,database=db)
    print("result is:")
    print(chat_preview_list)
    return chat_preview_list

@app.get("/search_user/{user_name}")
async def search_user(user_name:str):
    user=UserService.find_user(user_name,database=db)
    if user:
        return user.user_name
    else:
        return ""


@app.post("/add_friend/{user_name}/{friend_name}")
async def search_user(user_name:str,friend_name:str):
    pair_chat=ChatService.request_pair_chat(User(user_name),User(friend_name),database=db)
    return pair_chat.to_dict()


@app.get("/get_chat_room/{chat_room_id}")
async def getChat(chat_room_id:str):
    chats=ChatService.get_chat_room_by_id(chat_room_id,db)
    return chats.to_dict()


@app.get("/get_message/{msg_id}")
async def getChat(msg_id:str):
    message=ChatService.get_message_by_id(msg_id,db)
    return  message.to_dict()


@app.post("/send_text_message/{chat_room_id}/{user_name}/{text}")
async def chat_received(chat_room_id:str, user_name:str, text:str):
    user=User(user_name)
    print(f"pre chatroom id : {chat_room_id}")
    chat_room=ChatService.get_chat_room_by_id(chat_room_id,db)
    print(f"post chatroom id : {chat_room.getId()}")
    message = Message(user, chat_room,
                      TextMessage(text), datetime.datetime.now())
    res= await ChatService.send_message_async(message,db)
    return res

@app.post("/send_audio_message/{chat_room_id}/{user_name}/")
async def audio_received(chat_room_id:str, user_name:str, audio_file: UploadFile = Form(...)):
    # file_location = f"{audio_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(user.file.read())
    user = User(user_name)
    chat_room = ChatService.get_chat_room_by_id(chat_room_id, db)
    print(f"post chatroom id : {chat_room.getId()}")
    message = Message(user, chat_room,
                      AudioMessage(content=audio_file.file.read()), datetime.datetime.now())
    res = await ChatService.send_message_async(message, db)
    return res


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("inside websocket_endpoint")
    await websocket.accept()
    user_name=''
    data = await websocket.receive_text()
    print(f'data is: ', data)
    if (data.startswith('@user')):
        user_name = data.replace('@user', '')
        print(f'connect to username: {user_name}')
        ConnectionManager.connect(user_name, websocket)
    print(f'websocket for user {user_name} finished')
    try:
         while True:
             data = await websocket.receive_text()
    #
    #         else:
    #             d=data.split('@')
    #             print(f'user {user_name} send text {d[1]} to chat_room {d[0]}')
    #             message = Message(User(user_name), ChatService.get_chat_room_by_id(d[0], db),
    #                               TextMessage(d[1]), datetime.datetime.now())
    #             ChatService.send_message(message, db)
    except WebSocketDisconnect:
         ConnectionManager.disconnect(user_name)
        # await manager.broadcast(f"Client #{client_id} left the chat")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("inside websocket_endpoint")
    await websocket.accept()
    user_name=''
    data = await websocket.receive_text()
    print(f'data is: ', data)
    if (data.startswith('@user')):
        user_name = data.replace('@user', '')
        print(f'connect to username: {user_name}')
        ConnectionManager.connect(user_name, websocket)
    print(f'websocket for user {user_name} finished')
    try:
         while True:
             data = await websocket.receive_text()
    #
    #         else:
    #             d=data.split('@')
    #             print(f'user {user_name} send text {d[1]} to chat_room {d[0]}')
    #             message = Message(User(user_name), ChatService.get_chat_room_by_id(d[0], db),
    #                               TextMessage(d[1]), datetime.datetime.now())
    #             ChatService.send_message(message, db)
    except WebSocketDisconnect:
         ConnectionManager.disconnect(user_name)

# @app.websocket("/")
# async def websocket_endpoint(websocket: WebSocket):
#     print("inside websocket_endpoint")
#     await websocket.accept()
#     user_name=''
#     data = await websocket.receive_text()
#     print(f'data is: ', data)
#     if (data.startswith('@user')):
#         user_name = data.replace('@user', '')
#         print(f'connect to username: {user_name}')
#         ConnectionManager.connect(user_name, websocket)
#     print(f'websocket for user {user_name} finished')
#     try:
#          while True:
#              data = await websocket.receive_text()
#     #
#     #         else:
#     #             d=data.split('@')
#     #             print(f'user {user_name} send text {d[1]} to chat_room {d[0]}')
#     #             message = Message(User(user_name), ChatService.get_chat_room_by_id(d[0], db),
#     #                               TextMessage(d[1]), datetime.datetime.now())
#     #             ChatService.send_message(message, db)
#     except WebSocketDisconnect:
#          ConnectionManager.disconnect(user_name)