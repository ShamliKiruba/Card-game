import { useHistory } from 'react-router-dom';

export const ChangeRoute = (route) => {
    const history = useHistory();
    history.push(`/${route}`);
}

export const getCards = (obj) => {
    let arr = [];
    for(let i in obj) {
        arr.push(obj[i]);
    }
    return arr;
}