import { motion } from "framer-motion";
import { Brain, AlertCircle, Lightbulb } from "lucide-react";

function DiagnosisSection({ diagnosis }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.7 }}
      className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-2xl p-8 border-2 border-purple-200"
    >
      <h2 className="text-3xl font-bold text-purple-900 mb-6 flex items-center">
        <Brain className="w-8 h-8 mr-3" />
        AI-Powered Diagnosis
      </h2>

      <div className="space-y-6">
        {/* Root Cause */}
        <div className="bg-white rounded-xl p-6 shadow-md">
          <h3 className="text-xl font-semibold text-gray-800 mb-3 flex items-center">
            <AlertCircle className="w-5 h-5 mr-2 text-red-500" />
            Root Cause Analysis
          </h3>
          <div className="prose prose-lg max-w-none text-gray-700 whitespace-pre-wrap">
            {diagnosis.root_cause_analysis}
          </div>
        </div>

        {/* Business Impact */}
        <div className="bg-white rounded-xl p-6 shadow-md">
          <h3 className="text-xl font-semibold text-gray-800 mb-3 flex items-center">
            <Lightbulb className="w-5 h-5 mr-2 text-yellow-500" />
            Business Impact
          </h3>
          <p className="text-gray-700">{diagnosis.business_impact}</p>
        </div>

        {/* Full Diagnosis */}
        <div className="bg-white rounded-xl p-6 shadow-md">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">
            Complete Diagnosis
          </h3>
          <div className="prose prose-sm max-w-none text-gray-600 whitespace-pre-wrap leading-relaxed">
            {diagnosis.full_diagnosis}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default DiagnosisSection;
