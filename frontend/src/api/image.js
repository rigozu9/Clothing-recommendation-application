import api from "./api";

export const getImages = async (genderMode = "all", limit = 1000) => {
  const res = await api.get("/images", {
    params: {
      gender_mode: genderMode,
      limit: limit,
    },
  });

  return res.data;
};