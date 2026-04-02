import { useEffect, useState } from "react";
import { getRecommendations } from "../api/recommendations";

const RecommendationsPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [brokenImages, setBrokenImages] = useState(new Set());

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const res = await getRecommendations(2);
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

  if (loading) return <p>Loading recommendations...</p>;
  if (error) return <p>{error}</p>;
  if (!data) return <p>No data</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Recommendations</h1>

      <p>User ID: {data.user_id}</p>
      <p>Liked items count: {data.source_item_count}</p>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {data.recommendations
          .filter((item) => item.url && !brokenImages.has(item.image_id))
          .map((item) => (
            <div
              key={item.image_id}
              style={{
                border: "1px solid #ccc",
                padding: "10px",
                width: "200px",
              }}
            >
              <img
                src={item.url}
                alt={`Item ${item.image_id}`}
                style={{ width: "100%", height: "auto" }}
                onError={() => handleImageError(item.image_id)}
              />
              <p>ID: {item.image_id}</p>
              <p>Sim: {item.similarity.toFixed(3)}</p>
            </div>
          ))}
      </div>
    </div>
  );
};

export default RecommendationsPage;