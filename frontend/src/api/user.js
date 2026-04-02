import api from "./api";

export const createUser = async (userData) => {
  const res = await api.post("/users/register", userData);
  return res.data;
};

export const loginUser = async (data) => {
  const res = await api.post("/users/login", data);
  return res.data;
};