import React, { useEffect, useState } from "react";

import messageService, { MessageData } from "../services/messageService";
import { AxiosError, CanceledError } from "../services/apiClient";

interface Props {
  message_id: string;
  userName: string;
}

const user_init = {
  sender: "",
  reciever: "",
  content: {
    text: "loading",
  },
  date_time: "",
};

const ChatMessage = ({ message_id, userName }: Props) => {
  const [messageData, setMessageData] = useState<MessageData>(user_init);
  const [error, setErrot] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  useEffect(() => {
    setIsLoading(true);
    const { request, cancel } = messageService.getMessage(message_id);
    request
      .then(({ data: new_message }) => {
        console.log(new_message);
        setMessageData(new_message);
      })
      .catch((err) => {
        if (!(err instanceof CanceledError)) {
          setErrot((err as AxiosError).message);
        }
      })
      .finally(() => {
        setIsLoading(false);
      });
    return () => cancel();
  }, [message_id]);

  return (
    <>
      {isLoading && <div className="spinner-border"></div>}
      <li
        key={message_id}
        className={
          userName === messageData.sender
            ? "list-group-item list-group-item-success d-flex justify-content-between"
            : "list-group-item list-group-item-primary d-flex justify-content-end"
        }
      >
        {messageData.content.text}
        {userName === messageData.sender && (
          <button className="btn btn-outline-danger">Delete</button>
        )}
      </li>
      {error !== "" && (
        <li key={message_id} className="list-group-item list-group-item-danger">
          {error}
        </li>
      )}
    </>
  );
};

export default ChatMessage;
