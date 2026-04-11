import { useState } from "react";

const colorMap = {
  beige: "#D6C6A5",
  black: "#111111",
  blue: "#3B82F6",
  bronze: "#CD7F32",
  brown: "#8B5A2B",
  clear: "#E5E7EB",
  gold: "#D4AF37",
  gray: "#9CA3AF",
  green: "#22C55E",
  maroon: "#7F1D1D",
  orange: "#F97316",
  peach: "#FDBA74",
  pink: "#EC4899",
  purple: "#A855F7",
  red: "#EF4444",
  silver: "#C0C0C0",
  tan: "#D2B48C",
  teal: "#14B8A6",
  white: "#FFFFFF",
  yellow: "#EAB308",
};

const formatColorName = (name) => {
  return name
    .replace(/_/g, " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

const getSwatchStyle = (colorName) => {
  if (colorName === "multi_color") {
    return {
      background:
        "linear-gradient(135deg, #ef4444 0%, #f59e0b 20%, #eab308 40%, #22c55e 60%, #3b82f6 80%, #a855f7 100%)",
    };
  }

  return {
    backgroundColor: colorMap[colorName] || "#6B7280",
  };
};

const ColorsChart = ({ data }) => {
  const [showAll, setShowAll] = useState(false);
  const totalValue = data.reduce((sum, item) => sum + item.value, 0);

  const percentageData = data.map((item) => ({
    ...item,
    percentage: totalValue > 0 ? (item.value / totalValue) * 100 : 0,
  }));

  const topColors = percentageData.slice(0, 5);
  const otherColors = percentageData.slice(5);

  const othersPercentage = otherColors.reduce(
    (sum, item) => sum + item.percentage,
    0
  );

  const othersCount = otherColors.reduce((sum, item) => sum + item.value, 0);

  const displayData = showAll
    ? percentageData
    : othersPercentage > 0
    ? [
        ...topColors,
        {
          name: "Others",
          percentage: othersPercentage,
          value: othersCount,
          isOthers: true,
        },
      ]
    : topColors;

  return (
    <div className="bg-gray-800 rounded-xl shadow border border-gray-700 p-6 w-full max-w-5xl">
      <h2 className="text-2xl font-semibold mb-2">Your Top Colors</h2>
      <p className="text-gray-400 mb-6">
        Colors you tend to like most, ranked from strongest to weakest.
      </p>

      {displayData.length === 0 ? (
        <p className="text-gray-400">No color data available</p>
      ) : (
        <div className="space-y-5">
        {displayData.map((item) => (
          <div key={item.name}>
            {/* Rivi */}
            <div className="flex items-center justify-between mb-2 gap-4">
              <div className="flex items-center gap-3 min-w-0">
                {item.isOthers ? (
                  <div className="w-10 h-10 rounded-xl border border-gray-600 bg-gray-700 flex-shrink-0" />
                ) : (
                  <div
                    className={`w-10 h-10 rounded-xl flex-shrink-0 ${
                      item.name.toLowerCase() === "white" ||
                      item.name.toLowerCase() === "clear" ||
                      item.name.toLowerCase() === "silver"
                        ? "border border-gray-500"
                        : ""
                    }`}
                    style={getSwatchStyle(item.name)}
                  />
                )}

                <span className="text-lg font-medium text-white truncate">
                  {formatColorName(item.name)}
                </span>
              </div>

              <span className="text-lg font-semibold text-gray-200 flex-shrink-0">
                {Math.round(item.percentage)}%
              </span>
            </div>
            <div className="relative group mt-1">
              <div className="w-full h-4 bg-gray-700 rounded-full overflow-hidden transition">
                <div
                  className={`h-full rounded-full transition-all duration-200 group-hover:brightness-110 ${
                    item.isOthers ? "bg-gray-500" : ""
                  }`}
                  style={
                    item.isOthers
                      ? { width: `${item.percentage}%` }
                      : {
                          width: `${item.percentage}%`,
                          ...getSwatchStyle(item.name),
                        }
                  }
                />
              </div>

              <div className="absolute left-0 -top-12 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10">
                <div className="bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 shadow-lg text-sm whitespace-nowrap">
                  <p className="text-white font-medium">
                    {formatColorName(item.name)} — {Math.round(item.percentage)}%
                  </p>
                  <p className="text-gray-300">
                    {item.value} liked items
                  </p>
                </div>
              </div>
            </div>
            {item.isOthers && !showAll && (
              <button
                onClick={() => setShowAll(true)}
                className="mt-2 text-sm text-gray-300 hover:text-white underline"
              >
                Show all colors
              </button>
            )}
          </div>
        ))}
        {showAll && (
          <div className="mt-4">
            <button
              onClick={() => setShowAll(false)}
              className="text-sm text-gray-300 hover:text-white underline"
            >
              Show less
            </button>
          </div>
        )}
        </div>
      )}
    </div>
  );
};

export default ColorsChart;