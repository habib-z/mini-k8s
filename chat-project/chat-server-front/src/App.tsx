import { useEffect, useState, useContext, createContext } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";

import ChatRoomContent from "./components/ChatRoomContent";
import SignupForm from "./components/SignupForm";

const ws = new WebSocket("ws://localhost:3050/api/ws");
export const SocketContext = createContext(ws);

function App() {
  const socket = useContext(SocketContext);
  // socket.addEventListener("message", (event) => {
  //   const d = event.data;
  //   const constmsg_arr = String(d).split("@");
  //   console.log("message chat room id is ", constmsg_arr[1]);
  // });
  const [userName, setUserName] = useState("");
  useEffect(() => {
    if (userName !== "") {
      socket.send("@user" + userName);
    }
    // as soon as the component is mounted, do the following tasks:
    // emit USER_ONLINE event
    // subscribe to socket events
    // socket.on("JOIN_REQUEST_ACCEPTED", handleInviteAccepted);
    // return () => {
    //   // before the component is destroyed
    //   // unbind all event handlers used in this component
    //   socket.off("JOIN_REQUEST_ACCEPTED", handleInviteAccepted);
    // };
  }, [userName]);
  return (
    <>
      {userName === "" && (
        <SignupForm
          onLogedIn={(userName: string) => {
            setUserName(userName);
          }}
        />
      )}
      {userName !== "" && (
        <ChatRoomContent user_name={userName} chatRoomId="ali&sara" />
      )}
    </>
  );
}

export default App;
