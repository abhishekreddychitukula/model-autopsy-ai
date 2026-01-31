import { motion } from "framer-motion";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

function CorrelationChart({ data }) {
  const chartData = data?.points || [];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
      className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
    >
      <h3 className="text-xl font-bold text-gray-800 mb-2">
        Drift vs Impact Correlation
      </h3>
      <p className="text-sm text-gray-600 mb-4">
        Features in the top-right quadrant (high drift + high impact) are
        critical
      </p>
      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            type="number"
            dataKey="drift_score"
            name="Drift Score"
            label={{
              value: "Drift Score",
              position: "insideBottom",
              offset: -5,
            }}
            style={{ fontSize: "12px" }}
          />
          <YAxis
            type="number"
            dataKey="impact_score"
            name="Impact Score"
            label={{
              value: "Impact Score",
              angle: -90,
              position: "insideLeft",
            }}
            style={{ fontSize: "12px" }}
          />
          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            contentStyle={{
              backgroundColor: "white",
              border: "1px solid #e5e7eb",
              borderRadius: "8px",
              boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
            }}
            formatter={(value, name, props) => {
              if (name === "drift_score") return [value.toFixed(4), "Drift"];
              if (name === "impact_score") return [value.toFixed(4), "Impact"];
              return value;
            }}
            labelFormatter={(label, payload) => {
              return payload?.[0]?.payload?.feature || "";
            }}
          />
          <Scatter data={chartData} fill="#8b5cf6">
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.is_critical ? "#dc2626" : "#8b5cf6"}
                r={entry.is_critical ? 8 : 6}
              />
            ))}
          </Scatter>
        </ScatterChart>
      </ResponsiveContainer>
      <div className="flex justify-center space-x-6 mt-4 text-sm">
        <div className="flex items-center">
          <div className="w-3 h-3 bg-red-600 rounded-full mr-2"></div>
          <span className="text-gray-600">
            Critical (High Drift + High Impact)
          </span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-purple-500 rounded-full mr-2"></div>
          <span className="text-gray-600">Normal</span>
        </div>
      </div>
    </motion.div>
  );
}

export default CorrelationChart;
