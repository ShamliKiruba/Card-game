import React, { useState } from "react";

const JoinGame = () => {
  let [code, setCode] = useState("");

  const enterGame = (code) => {
    //make API call
    async function postData(
      url = "https://localhost:8080/enterGame",
      data = {}
    ) {
      const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify(data),
      });
      return response.json();
    }

    postData("https://localhost:5000/enterGame", { code }).then((data) => {
      console.log(data); // JSON data parsed by `data.json()` call
    });
  };

  return (
    <div>
      <p>Enter code</p>
      <input
        type="text"
        value={code}
        onChange={(event) => setCode(event.target.value)}
      />
      <button type="submit" onClick={enterGame()}>
        Submit
      </button>
    </div>
  );
};

export default JoinGame;
