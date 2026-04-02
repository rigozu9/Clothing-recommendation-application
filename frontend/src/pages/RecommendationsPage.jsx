import { useEffect, useState } from "react";
import { getRecommendations } from "../api/recommendations";
import Navbar from "../components/Navbar";

const RecommendationsPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [brokenImages, setBrokenImages] = useState(new Set());

  useEffect(() => {
    const fetchRecommendations = async () => {
      const userId = localStorage.getItem("user_id");

      if (!userId) {
        setError("You must be logged in to see recommendations");
        setLoading(false);
        return;
      }

      try {
        const res = await getRecommendations(userId);
        setData(res);
      } catch (err) {
        console.error(err);
        setError("Failed to load recommendations");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  const handleImageError = (imageId) => {
    setBrokenImages((prev) => new Set(prev).add(imageId));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white">
        <Navbar />
        <div className="max-w-7xl mx-auto px-6 py-6">
          <p className="text-gray-300">Loading recommendations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 text-white">
        <Navbar />
        <div className="max-w-7xl mx-auto px-6 py-6">
          <p className="text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-gray-900 text-white">
        <Navbar />
        <div className="max-w-7xl mx-auto px-6 py-6">
          <p className="text-gray-300">No data</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">My Recommendations</h1>
          <p className="text-gray-400 mt-2">
            Based on your liked items, here are the closest matches to your style.
          </p>
          <div className="mt-4 flex gap-6 text-sm text-gray-300">
            <p>User ID: {data.user_id}</p>
            <p>Liked items count: {data.source_item_count}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {data.recommendations
            .filter((item) => item.url && !brokenImages.has(item.image_id))
            .map((item) => (
              <div
                key={item.image_id}
                className="bg-gray-800 rounded-xl overflow-hidden shadow hover:scale-105 transition"
              >
                <img
                  src={item.url}
                  alt={`Item ${item.image_id}`}
                  className="w-full h-64 object-cover"
                  onError={() => handleImageError(item.image_id)}
                />

                <div className="p-3">
                  <p className="text-sm text-gray-300">ID: {item.image_id}</p>
                  <p className="text-sm font-medium mt-1">
                    Similarity: {item.similarity.toFixed(3)}
                  </p>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default RecommendationsPage;