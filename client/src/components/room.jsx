import React, { useEffect, useState } from 'react';
import { callAPI } from '../common/service';
import { get } from '../common/storage';
import { SOCKET } from '../common/socket';

function Room() {
    let [players, setPlayers] = useState([]);
    let [cards, setCards] = useState([]);
    let [game, setGame] = useState({});
    const sessionId = get("sessionId")
    useEffect(() => {
        const payload = {
            sessionId: sessionId,
            room: get('room')
        };
        // to get all players
        callAPI('POST', 'getPlayers', payload).then(data => {
            // setPlayers(data.players);
        });
        // to join room
        // Connected, let's sign-up for to receive messages for this room
        console.log("payload", payload)
        SOCKET.emit("join", payload);
        SOCKET.on("join_room_announcement", playerData => {
            console.log("as11d1111", playerData)
            setPlayers(playerData);
        });
        SOCKET.on("distribute_cards", res => {
            console.log("Cards", res)
            setGame(res)
            setCards(res.player_card[sessionId].cards)
        });
    }, []);
    return (
        <div className="board">
            {players.length > 0  && players.map(player => {
                    const cardCount = game.player_card && game.player_card[player].totalCards
                    return (
                        <div key={player}>
                            {
                                get('sessionId') === player ? (
                                    <div className="myDeck">
                                        {
                                            cards.map(card => {
                                                const symbol = card.split('_')[1];
                                                return (
                                                    <img src={`deck/${symbol}/${card}.png`}></img>
                                                )
                                            })
                                        }
                                        {player}
                                    </div>
                                ) : (
                                    <div className="others">
                                        {
                                            [...Array(cardCount)].map((e, i) => <img src={`design.png`}></img>)
                                        }
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
