import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const formatStyleName = (name) => {
  return name
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

const StylesChart = ({ data }) => {
  const totalValue = data.reduce((sum, item) => sum + item.value, 0);

  const topStyles = data.slice(0, 5);

  const radarData = topStyles.map((item) => ({
    subject: formatStyleName(item.name),
    value: totalValue > 0 ? (item.value / totalValue) * 100 : 0,
    rawValue: item.value,
  }));

  const summaryText = radarData
    .slice(0, 3)
    .map((item) => item.subject)
    .join(", ");

  return (
    <div className="bg-gray-800 rounded-xl shadow border border-gray-700 p-6 w-full max-w-5xl">
      <h2 className="text-2xl font-semibold mb-2">Your Style Direction</h2>

      <p className="text-gray-400 mb-6">
        {radarData.length > 0
          ? `Your style leans toward: ${summaryText}`
          : "Your style leans toward these directions based on your liked items."}
      </p>

      {radarData.length < 10 ? (
        <div className="rounded-xl border border-gray-700 bg-gray-900/60 px-4 py-3">
          <p className="text-gray-400 text-base">Like more items to get style insights</p>
        </div>
      ) : (
        <div className="w-full h-[650px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData}>
              <PolarGrid stroke="#4B5563" />
              <PolarAngleAxis
                dataKey="subject"
                tick={{ fill: "#D1D5DB", fontSize: 14 }}
              />
              <PolarRadiusAxis
                tick={{ fill: "#9CA3AF", fontSize: 12 }}
                axisLine={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#111827",
                  border: "1px solid #374151",
                  borderRadius: "12px",
                  color: "#FFFFFF",
                }}
                labelStyle={{ color: "#FFFFFF" }}
                formatter={(value, name, props) => [
                  `${Math.round(value)}%`,
                  props.payload.subject,
                ]}
              />
              <Radar
                name="Style"
                dataKey="value"
                stroke="#FFFFFF"
                fill="#FFFFFF"
                fillOpacity={0.25}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default StylesChart;