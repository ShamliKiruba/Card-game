import React from "react";
import { useHistory } from "react-router-dom";
import { get, set } from "../common/storage";
import { callAPI } from '../common/service';

function HostGame() {
	let history = useHistory();
	const changeRoute = (route) => {
		history.push(`/${route}`);
	};
    const create = () => {
		const payload = {
			sessionId: get("sessionId"),
		};
		callAPI('POST','createRoom', payload).then((data) => {
			console.log(data);
			set('room', data.room)
			changeRoute("room");
		});
    };
  return (
    <h1 onClick={create}>Create game</h1>
  );
}

export default HostGame;
