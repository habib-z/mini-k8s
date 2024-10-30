import React, { useEffect, useState } from "react";

import axios from "axios";

const url = import.meta.env.VITE_BACK_END_ADDRESS + ":8000/signup";
interface SingUpResData {
  result: boolean;
}
interface Props {
  onRequestChatSend: (chatText: string) => void;
}
const ChatInput = ({ onRequestChatSend }: Props) => {
  const [chatText, setChatText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);
  const handleSubmit = () => {
    setIsLoading(true);
    const user = { user_name: chatText };
    onRequestChatSend(chatText);
    setIsLoading(false);
  };

  // useEffect(() => {
  //   if (signUpResData.result) {
  //     onLogedIn(chatText);
  //   }
  // }, [signUpResData]);

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        handleSubmit();
      }}
    >
      <div className="mb-3">
        <input
          type="text"
          value={chatText}
          onChange={(data) => setChatText(data.target.value)}
          className="form-control"
          id="exampleInputEmail1"
        />
        {error && <p className="text-danger">error</p>}
      </div>
      <button disabled={isLoading} type="submit" className="btn btn-primary">
        Send
      </button>
    </form>
  );
};

export default ChatInput;
