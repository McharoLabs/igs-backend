import axios from "axios";
import { ROUTES } from "../routes/routes";
import { deleteTokenFromLocal } from "../state/auth/AuthSlice";

const apiClient = axios.create({
  baseURL: "https://rental.seranise.co.tz/api/v2",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && [401, 403].includes(error.response.status)) {
      sessionStorage.setItem(
        import.meta.env.REDIRECT_PATH,
        window.location.pathname
      );
      deleteTokenFromLocal();
      window.location.href = ROUTES.LOGIN.path;
    }

    return Promise.reject(error);
  }
);

export default apiClient;
