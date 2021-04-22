import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";


const Home = lazy(() => import("./components/home"));
const CreateGame = lazy(() => import("./components/createGame"));
const JoinGame = lazy(() => import("./components/joinGame"));
const Room = lazy(() => import("./components/room"));

const Routes = () => {
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
