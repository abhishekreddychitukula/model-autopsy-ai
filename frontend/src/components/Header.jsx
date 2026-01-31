import { motion } from "framer-motion";
import { Microscope, Github, FileText } from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function Header({ onReset, hasReport }) {
  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50 shadow-sm"
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div
            className="flex items-center space-x-3 cursor-pointer"
            onClick={onReset}
          >
            <div className="bg-gradient-to-br from-purple-600 to-blue-600 p-2 rounded-lg">
              <Microscope className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                Model Autopsy AI
              </h1>
              <p className="text-xs text-gray-600">
                Automated ML Failure Diagnosis
              </p>
            </div>
          </div>

          <nav className="flex items-center space-x-4">
            {hasReport && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onReset}
                className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg font-medium shadow-lg hover:shadow-xl transition-shadow"
              >
                New Analysis
              </motion.button>
            )}
            <a
              href={`${API_URL}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-gray-600 hover:text-purple-600 transition-colors"
              title="API Documentation"
            >
              <FileText className="w-5 h-5" />
            </a>
            <a
              href="https://github.com/abhishekreddychitukula/Model_Autopsy_AI"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-gray-600 hover:text-purple-600 transition-colors"
              title="GitHub"
            >
              <Github className="w-5 h-5" />
            </a>
          </nav>
        </div>
      </div>
    </motion.header>
  );
}

export default Header;
