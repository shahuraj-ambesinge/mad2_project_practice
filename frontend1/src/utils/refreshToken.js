import axios from "axios";

async function refreshAccessToken() {
    // get the refresh token from local storage
    let refresh_token =  localStorage.getItem('refresh_token')

    // set the Authorization header of the axios instance
    axios.defaults.headers.common['Authorization'] = "Bearer " + refresh_token

    try {
        // send a POST request to the server to refresh the access token
        let respone = await axios.post("http://127.0.0.1:8081/api/token/refresh");

        // get the new access token from the respone
        let new_access_token = respone.data.access_token;

        // store the new access token in local storage
        localStorage.setItem('access_token', new_access_token)

        // update the Authorization header of the axios instance
        axios.defaults.headers.common['Authorization'] = "Bearer " + new_access_token

    } catch (error) {
        // handle errors(eg invalid refresh token)
        console.error(error);
    }
    
}

export default refreshAccessToken;