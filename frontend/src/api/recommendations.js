import api from "./api";

export const getRecommendations = async (userId) => {
  const res = await api.get(`/recommendations/${userId}`);
  return res.data;
};