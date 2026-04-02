import api from "./api";

export const createUser = async (userData) => {
  const res = await api.post("/users", userData);
  return res.data;
};