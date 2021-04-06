import { useHistory } from 'react-router-dom';

export const ChangeRoute = (route) => {
    const history = useHistory();
    history.push(`/${route}`);
}