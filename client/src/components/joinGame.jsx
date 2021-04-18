import React, { useState } from "react";
import { get } from "../common/storage";

const JoinGame = () => {
  let [code, setCode] = useState("");

  const enterGame = () => {
    //make API call
    async function postData(
      url = "http://localhost:5000/enterRoom",
      data = {
        code,
        sessionId: get("sessionId"),
      }
    ) {
      console.log("request-->>", code);
      const response = await fetch(url, {
        method: "POST",
        "Access-Control-Allow-Origin": "http://localhost:5000",
        cache: "no-cache",
        headers: {},
        body: JSON.stringify({
          data: code,
        }),
      });
      return response.json();
    }

    postData("http://localhost:5000/enterRoom", { code }).then((data) => {
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
      <button type="submit" onClick={enterGame}>
        Submit
      </button>
    </div>
  );
};

export default JoinGame;
