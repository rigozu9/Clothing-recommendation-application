import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const MaterialsChart = ({ data }) => {
  return (
    <div className="bg-gray-800 rounded-xl shadow border border-gray-700 p-6 w-full max-w-5xl">
      <h2 className="text-2xl font-semibold mb-6">Favorite Materials</h2>

      {data.length === 0 ? (
        <p className="text-gray-400">No data available</p>
      ) : (
        <div className="w-full h-[500px]">
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
};

export default MaterialsChart;