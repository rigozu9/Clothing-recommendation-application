import api from "./api";

export const likeItem = async (userId, imageId) => {
  try {
    const response = await api.post(`/users/${userId}/like`, {
      image_id: imageId,
    });

    return response.data;
  } catch (error) {
    console.error("Error liking item:", error);
    throw error;
  }
};