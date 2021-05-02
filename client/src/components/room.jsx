import React, { useEffect, useState } from 'react';
import { callAPI } from '../common/service';
import { get } from '../common/storage';
import { SOCKET } from '../common/socket';
import { dummy } from '../data/dummy';

function Room() {
    let [opponents, setOpponents] = useState([]);
    // let [cards, setCards] = useState([]);
    let [game, setGame] = useState({});
    let [currentPlayer, setCurrentPlayer] = useState('');
    const sessionId = get("sessionId");
    const room = get("room");

    useEffect(() => {
        const payload = {
            sessionId,
            room
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
            setGame(res)
            // setCards(res.player_card[sessionId].cards)
        });
        SOCKET.on("player_turn", res => {
            console.log("player_turn", res)
            setCurrentPlayer(res);
        });
        SOCKET.on("drop_card", res => {
            console.log("drop_card", res)
            setGame(res.data);
        });
    }, []);

    const dropCard = (e) => {
        if(currentPlayer == sessionId) {
            let payload = {
                card: e.target.getAttribute('value'),
                id: sessionId,
                room: room
            };
            callAPI('POST', 'dropCard', payload).then(res => {
                console.log('successful', res)
                setGame(res.data)
                // setCards(res.data.player_card[sessionId].cards)
            });    
        }
    };

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
                                        {
                                            currentPlayer == opponent ? (
                                                <p>Your Turn</p>
                                            ) : (
                                                ''
                                            )
                                        }
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
                            game.player_card && game.player_card[sessionId].cards.map(card => {
                                const symbol = card.split('_')[1];
                                return (
                                    <img src={`deck/${symbol}/${card}.png`} value={card} onClick={(e) => dropCard(e)}></img>
                                );
                            })
                        }
                        {
                            currentPlayer == sessionId ? (
                                <p>Your turn</p>
                            ): (
                                ''
                            )
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
