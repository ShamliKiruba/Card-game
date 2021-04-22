import React, { useEffect } from "react";
import Routes from "../Routes";
import io from "socket.io-client";
import { set } from "../common/storage";

let endPoint = "http://localhost:5000";
let socket = io.connect(`${endPoint}`);
function App() {
  useEffect(() => {
    socket.on("connect", (data) => {
      console.log("connect callback",data);
    });

    socket.on("message", (data) => {
      console.log("message callback",data);
      set("sessionId", data);
    });
  }, []);
  return <Routes />;
};

export default App;
