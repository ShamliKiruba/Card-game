import React from 'react';
// import { ChangeRoute } from '../common/helper';
import { useHistory } from 'react-router-dom';

function Home() {
    let history = useHistory();
    const changeRoute = (route) => {
        history.push(`/${route}`);
    }
    return (
        <div>
            <div onClick={() => changeRoute('create')}>Host game</div>
            <div onClick={() => changeRoute('join')}>Join game</div>
        </div>
    )
}

export default Home;
