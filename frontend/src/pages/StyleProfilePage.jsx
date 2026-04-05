import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import Navbar from "../components/Navbar";
import { getUserStylePlot } from "../api/styleProfile";

const StyleProfilePage = () => {
  const [colorData, setColorData] = useState([]);
  const [materialData, setMaterialData] = useState([]);
  const [styleData, setStyleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
        const [colors, materials, styles] = await Promise.all([
          getUserStylePlot(userId, "color"),
          getUserStylePlot(userId, "material"),
          getUserStylePlot(userId, "style"),
        ]);

        setColorData(transformChartData(colors));
        setMaterialData(transformChartData(materials));
        setStyleData(transformChartData(styles));
      } catch (err) {
        console.error("Error fetching style profile:", err);
        setError("Failed to load style profile");
      } finally {
        setLoading(false);
      }
    };

    fetchStyleData();
  }, []);

  const ChartCard = ({ title, data }) => (
    <div className="bg-gray-800 rounded-xl shadow border border-gray-700 p-4">
      <h2 className="text-xl font-semibold mb-4">{title}</h2>

      {data.length === 0 ? (
        <p className="text-gray-400">No data available</p>
      ) : (
        <div className="w-full h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-6">
        <h1 className="text-3xl font-bold mb-6">My Style Profile</h1>

        {loading && <p className="text-gray-300">Loading style profile...</p>}
        {error && <p className="text-red-400">{error}</p>}

        {!loading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <ChartCard title="Favorite Colors" data={colorData} />
            <ChartCard title="Favorite Materials" data={materialData} />
            <ChartCard title="Favorite Styles" data={styleData} />
          </div>
        )}
      </div>
    </div>
  );
};

export default StyleProfilePage;