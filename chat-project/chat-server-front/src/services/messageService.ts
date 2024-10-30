import apiClient from "./apiClient";

export interface MessageData {
  sender: string;
  reciever: string;
  content: {
    text: string;
  };
  date_time: string;
}

class MessageService {
  getMessage(message_id: string) {
    const controller = new AbortController();
    const request = apiClient.get<MessageData>("/get_message/" + message_id, {
      signal: controller.signal,
    });
    return { request, cancel: () => controller.abort() };
  }
}

export default new MessageService();
