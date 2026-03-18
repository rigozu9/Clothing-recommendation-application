import api from "./api";

export const getImages = async () => {
  const res = await api.get("/images");
  return res.data;
};