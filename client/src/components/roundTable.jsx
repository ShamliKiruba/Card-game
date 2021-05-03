import React, { useEffect, useState } from 'react';

function RoundTable({data}) {
    let [cardList, setCardList] = useState([])
    useEffect(() => {
        let arr = [];
        for(let i in data) {
            arr.push(data[i]);
        }
        setCardList(arr);
    });

    return(
        <div class="activeRound">
            {cardList.map(card => {
                return(
                    <div>
                        {card}
                    </div>
                )
            })}
        </div>
    );
}

export default RoundTable;