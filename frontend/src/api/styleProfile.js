import api from "./api";

export const getUserStyleProfile = async (userId) => {
  const res = await api.get(`/users/${userId}/style-profile`);
  return res.data;
};