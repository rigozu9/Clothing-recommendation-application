import api from "./api";

export const getUserStylePlot = async (userId, tokenType = "color") => {
  const res = await api.get(`/users/${userId}/style-plot`, {
    params: { token_type: tokenType },
  });
  return res.data;
};