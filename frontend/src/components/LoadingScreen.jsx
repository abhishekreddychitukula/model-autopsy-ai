import { motion } from "framer-motion";
import { Loader2, Search, Brain, TrendingUp, CheckCircle2 } from "lucide-react";

function LoadingScreen() {
  const stages = [
    { icon: Search, text: "Validating data...", delay: 0 },
    { icon: TrendingUp, text: "Detecting drift...", delay: 1 },
    { icon: Brain, text: "Analyzing impact...", delay: 2 },
    { icon: CheckCircle2, text: "Generating diagnosis...", delay: 3 },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-2xl mx-auto text-center py-20"
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        className="inline-block mb-8"
      >
        <div className="bg-gradient-to-br from-purple-600 to-blue-600 p-8 rounded-full">
          <Loader2 className="w-16 h-16 text-white" />
        </div>
      </motion.div>

      <h2 className="text-3xl font-bold text-gray-800 mb-4">
        Running Autopsy Analysis
      </h2>
      <p className="text-gray-600 mb-12">
        Our AI is diagnosing your model failure...
      </p>

      <div className="space-y-4 max-w-md mx-auto">
        {stages.map((stage, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: stage.delay }}
            className="flex items-center space-x-4 p-4 bg-white rounded-xl shadow-md"
          >
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity, delay: stage.delay }}
              className="bg-gradient-to-br from-purple-500 to-blue-500 p-2 rounded-lg"
            >
              <stage.icon className="w-6 h-6 text-white" />
            </motion.div>
            <span className="text-gray-700 font-medium">{stage.text}</span>
            <motion.div
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: stage.delay,
              }}
              className="ml-auto"
            >
              <Loader2 className="w-5 h-5 text-purple-600 animate-spin" />
            </motion.div>
          </motion.div>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 4 }}
        className="mt-12 p-6 bg-purple-50 rounded-2xl border border-purple-200"
      >
        <p className="text-purple-800">
          <span className="font-semibold">Did you know?</span> Model Autopsy AI
          uses industry-standard statistical tests (KS-Test, PSI) combined with
          LLM-powered diagnosis to provide actionable insights in seconds.
        </p>
      </motion.div>
    </motion.div>
  );
}

export default LoadingScreen;
