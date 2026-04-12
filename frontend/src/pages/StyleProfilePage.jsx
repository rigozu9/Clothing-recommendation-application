import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import Navbar from "../components/Navbar";
import ColorsChart from "../components/ColorsChart";
import MaterialsChart from "../components/MaterialsChart";
import StylesChart from "../components/StylesChart";

import { getUserStyleProfile } from "../api/styleProfile";

const StyleProfilePage = () => {
  const [colorData, setColorData] = useState([]);
  const [materialData, setMaterialData] = useState([]);
  const [styleData, setStyleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchParams, setSearchParams] = useSearchParams();

  const viewMode = searchParams.get("view") || "color";

  const transformChartData = (res) => {
    return res.labels.map((label, i) => ({
      name: label,
      value: res.values[i],
    }));
  };

  useEffect(() => {
    const fetchStyleData = async () => {
      const userId = localStorage.getItem("user_id");

      if (!userId) {
        setError("You must be logged in to view your style profile");
        setLoading(false);
        return;
      }

      try {
        const profile = await getUserStyleProfile(userId);
        setColorData(transformChartData(profile.color));
        setMaterialData(transformChartData(profile.material));
        setStyleData(transformChartData(profile.style));
      } catch (err) {
        console.error("Error fetching style profile:", err);
        setError("Failed to load style profile");
      } finally {
        setLoading(false);
      }
    };

    fetchStyleData();
  }, []);

  const handleViewChange = (view) => {
    setSearchParams({ view });
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-6">
        <h1 className="text-3xl font-bold mb-6">My Style Profile</h1>

        <div className="flex justify-center gap-3 mb-6">
          <button
            onClick={() => handleViewChange("color")}
            className={`px-4 py-2 rounded-xl border transition ${
              viewMode === "color"
                ? "bg-white text-black border-white"
                : "border-white text-white hover:bg-white hover:text-black"
            }`}
          >
            Colors
          </button>

          <button
            onClick={() => handleViewChange("material")}
            className={`px-4 py-2 rounded-xl border transition ${
              viewMode === "material"
                ? "bg-white text-black border-white"
                : "border-white text-white hover:bg-white hover:text-black"
            }`}
          >
            Materials
          </button>

          <button
            onClick={() => handleViewChange("style")}
            className={`px-4 py-2 rounded-xl border transition ${
              viewMode === "style"
                ? "bg-white text-black border-white"
                : "border-white text-white hover:bg-white hover:text-black"
            }`}
          >
            Styles
          </button>
        </div>

        {loading && <p className="text-gray-300">Loading style profile...</p>}
        {error && <p className="text-red-400">{error}</p>}

        {!loading && !error && (
          <div className="flex justify-center items-center">
            {viewMode === "color" && <ColorsChart data={colorData} />}
            {viewMode === "material" && <MaterialsChart data={materialData} />}
            {viewMode === "style" && <StylesChart data={styleData} />}
          </div>
        )}
      </div>
    </div>
  );
};

export default StyleProfilePage;