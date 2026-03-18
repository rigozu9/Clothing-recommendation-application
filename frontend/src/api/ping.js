import api from "./api";

export const ping = async () => {
  try {
    const response = await api.get("/pong");
    return response.data;
  } catch (error) {
    console.error("Error pinging the server:", error);
    throw error;
  }
}