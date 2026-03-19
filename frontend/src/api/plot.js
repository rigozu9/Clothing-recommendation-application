import api from "./api";

export const getDataToPlot = async () => {
  const res = await api.get("/plotdata");
  return res.data;
};