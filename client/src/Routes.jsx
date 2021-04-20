import React, { Suspense, lazy, useEffect } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import io from "socket.io-client";
import { set } from "../src/common/storage";

let endPoint = "http://localhost:5000";
let socket = io.connect(`${endPoint}`);

const Home = lazy(() => import("./components/home"));
const CreateGame = lazy(() => import("./components/createGame"));
const JoinGame = lazy(() => import("./components/joinGame"));
const Room = lazy(() => import("./components/room"));

const Routes = () => {
  useEffect(() => {
    socket.on("connect", (data) => {
      console.log(data);
    });

    socket.on("message", (data) => {
      set("sessionId", data);
    });
  }, []);
  return (
    <Router>
      <Suspense fallback={<div>Loading...</div>}>
        <Switch>
          <Route exact path="/create" component={CreateGame} />
          <Route exact path="/join" component={JoinGame} />
          <Route exact path="/room" component={Room} />
          <Route exact path="/" component={Home} />
        </Switch>
      </Suspense>
    </Router>
  );
};

export default Routes;
