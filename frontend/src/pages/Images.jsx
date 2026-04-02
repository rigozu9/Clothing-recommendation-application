import { useEffect, useState } from "react";
import { getImages } from "../api/image";
import Navbar from "../components/Navbar";

const Images = () => {
  const [images, setImages] = useState([]);

  useEffect(() => {
    getImages().then(setImages);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-6">

        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">Browse Images</h1>
        </div>

        {/* Image grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {images.map((img) => (
            <div
              key={img.image_id}
              className="bg-gray-800 rounded-xl overflow-hidden shadow hover:scale-105 transition"
            >
              <img
                src={img.url}
                alt="clothing"
                className="w-full h-48 object-cover"
                onError={(e) => {
                  e.target.parentElement.style.display = "none";
                }}
              />
            </div>
          ))}
        </div>

      </div>
    </div>
  );
};

export default Images;