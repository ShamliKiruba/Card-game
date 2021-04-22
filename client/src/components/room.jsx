import React, { useEffect, useState } from 'react';
import { callAPI } from '../common/service';
import { get } from '../common/storage';
import io from "socket.io-client";

function Room() {
    let endPoint = "http://localhost:5000";
    let socketio = io.connect(`${endPoint}`, { query: get('room') });
    let [players, setPlayers] = useState([]);
    useEffect(() => {
        const payload = {
            sessionId: get("sessionId"),
            room: get('room')
        };
        // to get all players
        callAPI('POST', 'getPlayers', payload).then(data => {
            // setPlayers(data.players);
        });
        // to join room
        // Connected, let's sign-up for to receive messages for this room
        socketio.emit("join", payload);
        socketio.on("join_room_announcement", asd => {
            console.log("asd1111", asd)
            setPlayers(asd);
        });
    }, []);
    return (
        <div>
            {players.length > 0  && players.map(player => {
                    return (
                        <div key={player}>
                            {
                                get('sessionId') === player ? (
                                    <div className="myId">
                                        {player}
                                    </div>
                                ) : (
                                    <div className="others">
                                        {player}
                                    </div>
                                )}
                        </div>
                    )
                })
            }
        </div>
    )
}

export default Room;