import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getImages } from "../api/image";
import { likeItem } from "../api/user_like";
import Navbar from "../components/Navbar";

const Images = () => {
  const [images, setImages] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchParams, setSearchParams] = useSearchParams();

  const genderMode = searchParams.get("gender_mode") || "all";
  const limit = Number(searchParams.get("limit")) || 20;

  useEffect(() => {
    const fetchImages = async () => {
      setLoading(true);
      setError("");
      setCurrentIndex(0);

      try {
        const data = await getImages(genderMode, limit);
        setImages(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load images");
      } finally {
        setLoading(false);
      }
    };

    fetchImages();
  }, [genderMode, limit]);

  const handleGenderChange = (mode) => {
    setSearchParams({
      gender_mode: mode,
      limit: String(limit),
    });
  };

  const handleNext = () => {
    setCurrentIndex((prev) => prev + 1);
  };

  const handleDislike = () => {
    handleNext();
  };

  const handleLike = async () => {
    const userId = localStorage.getItem("user_id");

    if (!userId) {
      setError("You must be logged in to like items");
      return;
    }

    const currentImage = images[currentIndex];

    if (!currentImage) return;

    try {
      await likeItem(userId, currentImage.image_id);
      handleNext();
    } catch (err) {
      console.error(err);
      setError("Failed to like item");
    }
  };

  const currentImage = images[currentIndex];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">Browse Images</h1>
        </div>

        <div className="flex justify-center gap-3 mb-6">
          <button
            onClick={() => handleGenderChange("all")}
            className={`px-4 py-2 rounded-xl border transition ${
              genderMode === "all"
                ? "bg-white text-black border-white"
                : "border-white text-white hover:bg-white hover:text-black"
            }`}
          >
            All
          </button>

          <button
            onClick={() => handleGenderChange("male")}
            className={`px-4 py-2 rounded-xl border transition ${
              genderMode === "male"
                ? "bg-white text-black border-white"
                : "border-white text-white hover:bg-white hover:text-black"
            }`}
          >
            Men
          </button>

          <button
            onClick={() => handleGenderChange("female")}
            className={`px-4 py-2 rounded-xl border transition ${
              genderMode === "female"
                ? "bg-white text-black border-white"
                : "border-white text-white hover:bg-white hover:text-black"
            }`}
          >
            Women
          </button>
        </div>

        {loading && <p className="text-gray-300">Loading images...</p>}
        {error && <p className="text-red-400 mb-4">{error}</p>}

        {!loading && !currentImage && (
          <div className="flex justify-center items-center py-20">
            <p className="text-gray-300 text-lg">No more images to show</p>
          </div>
        )}

        {!loading && currentImage && (
          <div className="flex justify-center">
            <div className="bg-gray-800 rounded-2xl overflow-hidden shadow-xl w-full max-w-md border border-gray-700">
              <img
                src={currentImage.url}
                alt="clothing"
                className="w-full h-[500px] object-cover"
                onError={() => {
                  handleNext();
                }}
              />

              <div className="p-4 flex justify-center gap-6">
                <button
                  onClick={handleDislike}
                  className="w-16 h-16 rounded-full border border-red-400 text-red-400 text-2xl hover:bg-red-400 hover:text-white transition"
                >
                  ✕
                </button>

                <button
                  onClick={handleLike}
                  className="w-16 h-16 rounded-full border border-green-400 text-green-400 text-2xl hover:bg-green-400 hover:text-white transition"
                >
                  ♥
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Images;