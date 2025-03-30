import axios from "axios";

// Function to refresh access token
const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem("refreshToken");

  if (!refreshToken) {
    console.log("No refresh token found. Logging out.");
    return null;
  }

  try {
    const response = await axios.post(`${process.env.REACT_APP_API_URL}token/refresh/`, {
      refresh: refreshToken,
    });

    const { access } = response.data;
    localStorage.setItem("accessToken", access);
    return access;
  } catch (error) {
    console.error("Token refresh failed. Redirecting to login.");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    window.location.href = "/login"; // Redirect to login
    return null;
  }
};

// Axios interceptor to automatically attach token to requests
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Axios interceptor to handle token expiration and auto-refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newAccessToken = await refreshAccessToken();

      if (newAccessToken) {
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return axios(originalRequest); // Retry request with new token
      }
    }

    return Promise.reject(error);
  }
);

export { refreshAccessToken };