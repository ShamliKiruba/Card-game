import React, { useEffect, useState } from 'react';
import { callAPI } from '../common/service';
import { get } from '../common/storage';
import { SOCKET } from '../common/socket';
import { dummy } from '../data/dummy';

function Room() {
    let [opponents, setOpponents] = useState([]);
    let [cards, setCards] = useState([]);
    let [game, setGame] = useState({});
    const sessionId = get("sessionId");
    useEffect(() => {
        const payload = {
            sessionId: sessionId,
            room: get('room')
        };
        // to get all players
        callAPI('POST', 'getPlayers', payload).then(data => {
            // all players
            // setPlayers(data.players);
        });
        SOCKET.emit("join", payload);
        SOCKET.on("join_room_announcement", playerData => {
            let opponents = playerData.filter(player => player != sessionId);
            setOpponents(opponents);
        });
        SOCKET.on("distribute_cards", res => {
            console.log("Cards", res)
            setGame(res)
            setCards(res.player_card[sessionId].cards)
        });
    }, []);
    return (
        <div className="board-container"> 
            {
                opponents.length == 3 ? (
                    <div>
                        {opponents.length > 0  && opponents.map(opponent => {
                            const cardCount = game.player_card && game.player_card[opponent].totalCards
                            return (
                                <div className='opponent' key={opponent}>
                                    <div className="others">
                                        <p>{opponent}</p>
                                        {
                                            [...Array(cardCount)].map((e, i) => <img src={`design.png`}></img>)
                                        }
                                    </div>
                                </div>
                            )
                        })
                    }
                    <div className="myDeck">
                        {
                            cards.map(card => {
                                const symbol = card.split('_')[1];
                                return (
                                    <img src={`deck/${symbol}/${card}.png`}></img>
                                );
                            })
                        }
                        <p>{sessionId}</p>
                    </div>
                    </div>
                ) : (
                    <div>
                        Waiting for everyone to join
                    </div>
                )
            }
        </div>
    )
}

export default Room;
