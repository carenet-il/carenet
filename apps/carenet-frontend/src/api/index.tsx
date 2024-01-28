import { Axios } from "axios";

const API_URL = "https://api-carenet.koyeb.app";

const apiClient = new Axios({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
