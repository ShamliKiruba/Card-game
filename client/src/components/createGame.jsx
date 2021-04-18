import React from "react";

const createGame = () => {
  const create = () => {
    //make API call
    async function postData(
      url = "http://localhost:5000/createRoom",
      data = {}
    ) {
      const response = await fetch(url, {
        method: "GET",
        "Access-Control-Allow-Origin": "http://localhost:5000",
        cache: "no-cache",
      });
      return response.json();
    }

    postData("http://localhost:5000/createRoom").then((data) => {
      console.log(data); // JSON data parsed by `data.json()` call
    });
  };
  return <div onClick={create}>Create game</div>;
};

export default createGame;
