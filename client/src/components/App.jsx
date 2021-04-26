// import React, { useEffect } from "react";
// import Routes from "../Routes";
// import io from "socket.io-client";
// import { set } from "../common/storage";
// import { socketOn } from '../common/socket';

// let endPoint = "http://localhost:5000";
// let socket = io.connect(`${endPoint}`);
// function App() {
// 	useEffect(() => {
// 		socketOn('connect', (response) => {
// 			console.log("connect callback", response);
// 		});
// 		socketOn('message', (data) => {
// 			console.log("message callback",data);
// 			set("sessionId", data);
// 		});
// 	}, []);
// 	return <Routes />;
// };

// export default App;


import React, { useEffect } from "react";
import Routes from "../Routes";
import { SOCKET } from '../common/socket';
import { set } from "../common/storage";

function App() {
  useEffect(() => {
    SOCKET.on("connect", (data) => {
      console.log("connect callback",data);
    });

    SOCKET.on("message", (data) => {
      console.log("message callback",data);
      set("sessionId", data);
    });
  }, []);
  return <Routes />;
};

export default App;
