import { motion } from "framer-motion";

function StatCard({ icon: Icon, label, value, total, color, index }) {
  const colorClasses = {
    red: "from-red-500 to-red-600",
    orange: "from-orange-500 to-orange-600",
    purple: "from-purple-500 to-purple-600",
    blue: "from-blue-500 to-blue-600",
    green: "from-green-500 to-green-600",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ y: -5 }}
      className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all border border-gray-100"
    >
      <div className="flex items-start justify-between mb-4">
        <div
          className={`bg-gradient-to-br ${colorClasses[color]} p-3 rounded-xl`}
        >
          <Icon className="w-6 h-6 text-white" />
        </div>
        {total && <div className="text-sm text-gray-500">/ {total}</div>}
      </div>
      <div className="text-3xl font-bold text-gray-800 mb-1">{value}</div>
      <div className="text-sm text-gray-600">{label}</div>
    </motion.div>
  );
}

export default StatCard;
