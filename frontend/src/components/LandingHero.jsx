import { motion } from "framer-motion";
import { Sparkles, TrendingDown, Brain, Zap, CheckCircle } from "lucide-react";

function LandingHero({ onGetStarted }) {
  const features = [
    { icon: TrendingDown, text: "Detect Data Drift", color: "text-red-500" },
    { icon: Brain, text: "AI-Powered Diagnosis", color: "text-purple-500" },
    { icon: Zap, text: "Instant Analysis", color: "text-yellow-500" },
    { icon: CheckCircle, text: "Actionable Insights", color: "text-green-500" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center mb-16"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring" }}
          className="inline-block mb-6"
        >
          <div className="bg-gradient-to-br from-purple-600 to-blue-600 p-6 rounded-3xl shadow-2xl">
            <Sparkles className="w-16 h-16 text-white" />
          </div>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-6xl font-extrabold mb-6 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 bg-clip-text text-transparent"
        >
          Model Autopsy AI
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-2xl text-gray-600 mb-4"
        >
          Automated Root Cause Analysis for ML Model Failures
        </motion.p>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="text-lg text-gray-500 mb-12 max-w-3xl mx-auto"
        >
          Stop wasting days debugging. Upload your data and get instant
          AI-powered diagnosis of why your model failed, which features drifted,
          and what to do next.
        </motion.p>

        <motion.button
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.9, type: "spring" }}
          whileHover={{ scale: 1.05, boxShadow: "0 20px 40px rgba(0,0,0,0.2)" }}
          whileTap={{ scale: 0.95 }}
          onClick={onGetStarted}
          className="px-12 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white text-xl font-bold rounded-full shadow-2xl hover:shadow-purple-500/50 transition-all"
        >
          Start Diagnosis →
        </motion.button>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16"
      >
        {features.map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 + index * 0.1 }}
            whileHover={{ y: -5 }}
            className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all border border-gray-100"
          >
            <feature.icon className={`w-10 h-10 mb-4 ${feature.color}`} />
            <h3 className="font-semibold text-gray-800">{feature.text}</h3>
          </motion.div>
        ))}
      </motion.div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-3xl p-12 text-center"
      >
        <h2 className="text-3xl font-bold text-gray-800 mb-6">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              step: "1",
              title: "Upload Data",
              desc: "Training baseline & production data",
            },
            {
              step: "2",
              title: "AI Analysis",
              desc: "Drift detection & impact scoring",
            },
            {
              step: "3",
              title: "Get Insights",
              desc: "Actionable recommendations",
            },
          ].map((item, index) => (
            <div key={index} className="relative">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-600 to-blue-600 text-white text-2xl font-bold rounded-full mb-4">
                {item.step}
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {item.title}
              </h3>
              <p className="text-gray-600">{item.desc}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}

export default LandingHero;
