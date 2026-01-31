import { motion } from "framer-motion";
import {
  AlertTriangle,
  TrendingDown,
  Target,
  Brain,
  Download,
  RefreshCw,
} from "lucide-react";
import html2pdf from "html2pdf.js";
import DriftChart from "./charts/DriftChart";
import ImpactChart from "./charts/ImpactChart";
import CorrelationChart from "./charts/CorrelationChart";
import StatCard from "./StatCard";
import DiagnosisSection from "./DiagnosisSection";

function Dashboard({ report, onNewAnalysis }) {
  const {
    executive_summary,
    drift_analysis,
    impact_analysis,
    diagnosis,
    timeline,
  } = report;

  const handleExport = () => {
    const element = document.getElementById("dashboard-content");
    const opt = {
      margin: 10,
      filename: `model-autopsy-report-${new Date().toISOString().split("T")[0]}.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true, letterRendering: true },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
    };
    html2pdf().set(opt).from(element).save();
  };

  const stats = [
    {
      icon: TrendingDown,
      label: "Features Drifted",
      value: drift_analysis.summary.drifted_features_count,
      total: drift_analysis.summary.total_features_analyzed,
      color: "red",
    },
    {
      icon: AlertTriangle,
      label: "Severe Drift",
      value: drift_analysis.summary.severe_drift_count,
      color: "orange",
    },
    {
      icon: Target,
      label: "High Impact",
      value: impact_analysis.summary.high_impact_count,
      color: "purple",
    },
    {
      icon: Brain,
      label: "Critical Features",
      value: timeline.summary.critical_features,
      color: "blue",
    },
  ];

  const getSeverityColor = (severity) => {
    if (severity?.includes("CRITICAL"))
      return "text-red-600 bg-red-50 border-red-200";
    if (severity?.includes("HIGH"))
      return "text-orange-600 bg-orange-50 border-orange-200";
    if (severity?.includes("MODERATE"))
      return "text-yellow-600 bg-yellow-50 border-yellow-200";
    return "text-green-600 bg-green-50 border-green-200";
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-7xl mx-auto space-y-8"
      id="dashboard-content"
    >
      {/* Header */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200"
      >
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-4xl font-bold text-gray-800 mb-3">
              Autopsy Report Complete
            </h1>
            <p className="text-lg text-gray-600 mb-4">
              {executive_summary.summary}
            </p>
            <div
              className={`inline-flex items-center px-4 py-2 rounded-full border-2 font-semibold ${getSeverityColor(executive_summary.severity)}`}
            >
              <AlertTriangle className="w-5 h-5 mr-2" />
              {executive_summary.severity}
            </div>
          </div>
          <div className="flex space-x-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleExport}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-medium flex items-center space-x-2 transition-colors"
            >
              <Download className="w-4 h-4" />
              <span>Export</span>
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onNewAnalysis}
              className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium flex items-center space-x-2 shadow-lg"
            >
              <RefreshCw className="w-4 h-4" />
              <span>New Analysis</span>
            </motion.button>
          </div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} index={index} />
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DriftChart data={drift_analysis.drift_leaderboard} />
        <ImpactChart data={impact_analysis.impact_leaderboard} />
      </div>

      {/* Correlation Chart */}
      <CorrelationChart data={report.visualizations?.correlation_data} />

      {/* Critical Features */}
      {timeline.critical_features?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl p-8 border-2 border-red-200"
        >
          <h2 className="text-2xl font-bold text-red-900 mb-4 flex items-center">
            <AlertTriangle className="w-6 h-6 mr-2" />
            Critical Features Identified
          </h2>
          <p className="text-red-800 mb-6">
            These features exhibit both significant drift AND high impact on
            predictions
          </p>
          <div className="flex flex-wrap gap-3">
            {timeline.critical_features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="px-6 py-3 bg-white rounded-full font-semibold text-red-700 shadow-lg border-2 border-red-300"
              >
                {feature}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* AI Diagnosis */}
      <DiagnosisSection diagnosis={diagnosis} />

      {/* Recommendations */}
      {timeline.recommendations?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-blue-50 rounded-2xl p-8 border border-blue-200"
        >
          <h2 className="text-2xl font-bold text-blue-900 mb-6 flex items-center">
            <Target className="w-6 h-6 mr-2" />
            Recommended Actions
          </h2>
          <div className="space-y-3">
            {timeline.recommendations.map((rec, index) => (
              <motion.div
                key={index}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.9 + index * 0.1 }}
                className="flex items-start space-x-3 p-4 bg-white rounded-xl shadow-sm"
              >
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                  {index + 1}
                </div>
                <p className="text-gray-700 flex-1">{rec}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}

export default Dashboard;
