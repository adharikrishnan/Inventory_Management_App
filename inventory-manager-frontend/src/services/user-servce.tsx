import axios from "axios";


const API_URL = "http://localhost:8000/";

export const UserService = {
    getUserCount: async () => {
        try {
            const response = await axios.post(`${API_URL}users/count`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true, // Include credentials (cookies) in the request
            });

            if (response.status !== 200) {
                throw new Error("Failed to fetch user count");
            }

            const data = await response.data;
            return data.user_count;
        } catch (error) {
            throw error;
        }
    },
};