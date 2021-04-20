import React, { useState } from "react";
import { get, set } from "../common/storage";
import { useHistory } from "react-router-dom";
import { callAPI } from "../common/service";

function JoinGame() {
	let [code, setCode] = useState("");
	let history = useHistory();
	const changeRoute = (route) => {
		history.push(`/${route}`);
	};
	const enterGame = () => {
		const payload = {
			data: code,
			sessionId: get("sessionId"),
		};
		callAPI('POST', 'enterRoom', payload).then(data => {
			console.log(data);
			set('room', data.room)
			changeRoute("room");
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
}

export default JoinGame;
