import React, { useEffect, useState } from 'react';
import { callAPI } from '../common/service';
import { get } from '../common/storage';
import { SOCKET } from '../common/socket';
import RoundTable from './roundTable';

function Room() {
    let [opponents, setOpponents] = useState([]);
    // let [cards, setCards] = useState([]);
    let [players, setPlayers] = useState([]);
    let [roundTable, setRoundTable] = useState({});
    let [game, setGame] = useState({});
    let [stashedCards, setStashedCards] = useState([]);
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
            setPlayers(data.players);
        });
        SOCKET.emit("join", payload);
        SOCKET.on("join_room_announcement", playerData => {
            let opponents = playerData.filter(player => player !== sessionId);
            setOpponents(opponents);
        });
        SOCKET.on("distribute_cards", res => {
            setGame(res);
            console.log("game", res);
            setRoundTable(res.current_round);
            setStashedCards(res.center_cards);
            // setCards(res.player_card[sessionId].cards)
        });
        SOCKET.on("player_turn", res => {
            console.log("player_turn", res)
            setCurrentPlayer(res);
            setTimeout(() => {
                console.log('after 10s wait')
                    // let cardList = game.player_card[res];
                    // if(Object.keys(game.current_round).length) {
                    //     let init_draw = game.current_round[1].card.split('_')[1]
                    //     let presentCards = cardList.filter(card => (init_draw == card.split('_')[1]))
                    //     if(presentCards.length) {
                    //         const randomIndex = Math.floor(Math.random() * presentCards.length);
                    //         let cardToDrop = presentCards[randomIndex]
                    //         dropCard(cardToDrop)
                    //     //  emit drop_card with this card
                    //     } else { 
                    //         // skip the turn
                    //     }
                    // }
                    // if time exceeds check if the player have the symbol supposed to be drawn
                    // if yes chose random card and drop - loser move
                    // if not miss a chance, he will lose a winning chance
            }, 5000);
        });
        SOCKET.on("drop_card", res => {
            console.log("Pusher dropCard", res)
            setGame(res.data);
            setRoundTable(res.data.current_round);
            setStashedCards(res.data.center_cards);
        });
    }, []);

    const dropCard = (cardToDrop) => {
        if(currentPlayer === sessionId) {
            let payload = {
                card: cardToDrop,
                id: sessionId,
                room: room,
                game
            };
            callAPI('POST', 'dropCard', payload).then(res => {
                console.log('API dropCard', res)
                setGame(res.data)
                setRoundTable(res.data.current_round);
                setStashedCards(res.data.center_cards);
                // setCards(res.data.player_card[sessionId].cards)
            });    
        }
    };

    return (
        <div className="board-container"> 
            {
                opponents.length === 3 ? (
                    <div>
                        {opponents.length > 0  && opponents.map(opponent => {
                            const cardCount = game.player_card && game.player_card[opponent].totalCards
                            return (
                                <div className='opponent' key={opponent}>
                                    <div className="others">
                                        {
                                            currentPlayer === opponent ? (
                                                <p>Opponent's Turn</p>
                                            ) : (
                                                ''
                                            )
                                        }
                                        <p>{opponent}</p>
                                        {
                                            [...Array(cardCount)].map((e, i) => <img key={i} alt="hidden cards" src={`design.png`}></img>)
                                        }
                                    </div>
                                </div>
                            )
                        })
                    }
                    <div className="myDeck">
                        {
                            currentPlayer === sessionId ? (
                                <p>Your turn</p>
                            ): (
                                ''
                            )
                        }
                        <p>{sessionId}</p>
                        <div className="myCards">
                            {
                                game.player_card && game.player_card[sessionId].cards.map((card, index) => {
                                    const symbol = card.split('_')[1];
                                    return (
                                        <img alt="my cards" key={index} src={`deck/${symbol}/${card}.png`} value={card} onClick={(e) => dropCard(e.target.getAttribute('value'))}></img>
                                    );
                                })
                            }
                        </div>
                        
                    </div>
                    </div>
                ) : (
                    <div>
                        Waiting for everyone to join
                    </div>
                )
            }
            <div>
                {/* {Object.keys(game).length > 0 ? <RoundTable data={game.set_round_one} /> : ''} */}
                {/* roundTable ex:  {1: {5pPgacn5M7234OW8AAAZ: "Q_club"}, 2: {le_DYjBZmJzfQBgBAAAb: "K_heart"}} */}
                {Object.keys(roundTable).length? (
                    <div className="activeRound">
                        {Object.keys(roundTable).map(key => {
                            let turn = roundTable[key];
                            let card = turn.card;
                            const symbol = card.split('_')[1];
                            return(
                                <div>
                                    <img alt="current round cards" src={`deck/${symbol}/${card}.png`} value={card}></img>
                                </div>
                            )
                        })}
                    </div>
                ) : ''}
            </div>
            <div>
                {/* {Object.keys(game).length > 0 ? <RoundTable data={game.set_round_one} /> : ''} */}
                {/* roundTable ex:  {1: {5pPgacn5M7234OW8AAAZ: "Q_club"}, 2: {le_DYjBZmJzfQBgBAAAb: "K_heart"}} */}
                {/* {(stashedCards.length > 0) ? (
                    <div className="stashedCards">
                        {stashedCards.map((draw, index) => {
                            return (
                                <p>Round {index + 1} over</p>
                            )
                        })}
                    </div>
                ) : ''} */}
                <p>Round {stashedCards.length} over</p>
            </div>
        </div>
    )
}

export default Room;
