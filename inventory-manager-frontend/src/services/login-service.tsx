import axios from "axios";


const API_URL = "http://localhost:8080/api/";

export const LoginService = {
    login: async (username: string, password: string) => {
        try {
            const response = await axios.post(`${API_URL}login`, { username, password });
            if (response.status !== 200) {
                throw new Error("Login failed");
            }
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}