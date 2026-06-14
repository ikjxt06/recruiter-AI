import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "/api/v1"
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("talentiq_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("talentiq_token");
      window.dispatchEvent(new Event("talentiq:logout"));
    }
    return Promise.reject(error);
  }
);
