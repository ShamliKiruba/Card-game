import { DOMAIN } from './constants';

export const callAPI = async (method, url, payload) => {
    const response = await fetch(DOMAIN + url, {
        method: method,
        "Access-Control-Allow-Origin": "http://localhost:5000",
        cache: "no-cache",
        body: JSON.stringify(payload),
    });
    return response.json();
};