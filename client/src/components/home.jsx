import React from "react";
import { useHistory } from "react-router-dom";

function Home() {
  let history = useHistory();
  const changeRoute = (route) => {
    history.push(`/${route}`);
  };
  return (
    <div>
      {/* <img src="deck/club/2_club.png"></img> */}
      <h1 onClick={() => changeRoute('create')}>Host game</h1>
      <h1 onClick={() => changeRoute('join')}>Join game</h1>
    </div>
  );
}

export default Home;
