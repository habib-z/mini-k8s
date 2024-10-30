import React, { useContext, useEffect, useState } from "react";
import ChatMessage from "./ChatMessage";
import apiClient from "../services/apiClient";
import ChatInput from "./ChatInput";
import { SocketContext } from "../App";

interface ChatRoomData {
  users: string[];
  messages: string[];
  message_user_seen: { [key: string]: boolean[] };
}
interface Props {
  user_name: string;
  chatRoomId: string;
}

const ChatRoomContent = ({ user_name, chatRoomId }: Props) => {
  const socket = useContext(SocketContext);
  socket.addEventListener("message", (event) => {
    const d = event.data;
    const constmsg_arr = String(d).split("@");
    console.log("message chat room id is ", constmsg_arr[1]);
    console.log("chat room id is ", chatRoomId);
    if (chatRoomId === constmsg_arr[1]) {
      console.log("new message came");
      seChatRoomData({
        ...chatRoomData,
        messages: [...chatRoomData.messages, d],
      });
    }
  });
  const [chatRoomData, seChatRoomData] = useState<ChatRoomData>({
    users: [],
    messages: [],
    message_user_seen: {},
  });
  useEffect(() => {
    console.log("connecting to " + chatRoomId);
    if(chatRoomId===''){
      return;
    }
    apiClient
      .get("/get_chat_room/" + chatRoomId)
      .then((res) => {
        console.log(res.data);
        seChatRoomData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [chatRoomId]);

  const handleRequestChat = (text: string) => {
    console.log("send text", text);
    apiClient
      .post("/send_text_message/" + chatRoomId + "/" + user_name + "/" + text)
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <>
      <ul className="list-group">
        {chatRoomData.messages.map((message) => (
          <ChatMessage message_id={message} userName={user_name}></ChatMessage>
        ))}
      </ul>
      <ChatInput onRequestChatSend={handleRequestChat} />
    </>
  );
};

export default ChatRoomContent;
