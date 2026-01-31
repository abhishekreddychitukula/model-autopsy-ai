import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

function ImpactChart({ data }) {
  const chartData =
    data?.slice(0, 10).map((item) => ({
      name: item.feature,
      score: item.impact_score,
      level: item.impact_level,
    })) || [];

  const getColor = (level) => {
    switch (level) {
      case "High":
        return "#7c3aed";
      case "Moderate":
        return "#3b82f6";
      case "Low":
        return "#8b5cf6";
      default:
        return "#6b7280";
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
    >
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        Feature Impact Scores
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis type="number" style={{ fontSize: "12px" }} />
          <YAxis
            dataKey="name"
            type="category"
            width={100}
            style={{ fontSize: "12px" }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
              boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
            }}
          />
          <Bar dataKey="score" radius={[0, 8, 8, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.level)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex justify-center space-x-6 mt-4 text-sm">
        <div className="flex items-center">
          <div className="w-3 h-3 bg-purple-600 rounded-full mr-2"></div>
          <span className="text-gray-600">High</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
          <span className="text-gray-600">Moderate</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-purple-400 rounded-full mr-2"></div>
          <span className="text-gray-600">Low</span>
        </div>
      </div>
    </motion.div>
  );
}

export default ImpactChart;
