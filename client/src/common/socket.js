import io from "socket.io-client";

let endPoint = "http://localhost:5000";
export const SOCKET = io.connect(`${endPoint}`);
