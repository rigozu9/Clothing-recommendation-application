import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { getDataToPlot } from "../api/plot"; // adjust path if needed

const PlotComponent = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getDataToPlot();

        // transform backend format → recharts format
        const formatted = res.labels.map((label, i) => ({
          name: label,
          value: res.values[i],
        }));

        setData(formatted);
      } catch (err) {
        console.error("Error fetching plot data:", err);
      }
    };

    fetchData();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Style Vector Example</h2>

      <BarChart width={600} height={300} data={data}>
        <CartesianGrid />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" />
      </BarChart>
    </div>
  );
};

export default PlotComponent;