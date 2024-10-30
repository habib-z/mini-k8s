import React from "react";
import * as io from "socket.io-client";
export const socket = io.connect(import.meta.env.VITE_BACK_END_ADDRESS + ":8000/ws");
export const SocketContext = React.createContext(socket);
