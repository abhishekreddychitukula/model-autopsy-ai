import { motion } from "framer-motion";
import { Upload, File, CheckCircle, AlertCircle, Play } from "lucide-react";

function FileUpload({ files, onFilesChange, onAnalyze, error }) {
  const handleFileChange = (type) => (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith(".csv")) {
      onFilesChange({ ...files, [type]: file });
    }
  };

  const fileTypes = [
    {
      key: "train",
      label: "Training Data",
      desc: "Baseline model training data",
      icon: "📊",
    },
    {
      key: "prod_old",
      label: "Production (Old)",
      desc: "Data before model failure",
      icon: "⏮️",
    },
    {
      key: "prod_new",
      label: "Production (New)",
      desc: "Data after model failure",
      icon: "🔴",
    },
  ];

  const allFilesUploaded = files.train && files.prod_old && files.prod_new;

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h2 className="text-4xl font-bold text-gray-800 mb-4">
          Upload Your Data
        </h2>
        <p className="text-lg text-gray-600">
          Upload three CSV files to begin the autopsy analysis
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {fileTypes.map((type, index) => (
          <motion.div
            key={type.key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="relative"
          >
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange(type.key)}
              className="hidden"
              id={`file-${type.key}`}
            />
            <label
              htmlFor={`file-${type.key}`}
              className={`block p-6 rounded-2xl border-2 border-dashed cursor-pointer transition-all ${
                files[type.key]
                  ? "border-green-500 bg-green-50 hover:bg-green-100"
                  : "border-gray-300 bg-white hover:border-purple-500 hover:bg-purple-50"
              }`}
            >
              <div className="text-center">
                <div className="text-4xl mb-3">{type.icon}</div>
                <h3 className="font-semibold text-gray-800 mb-1">
                  {type.label}
                </h3>
                <p className="text-sm text-gray-500 mb-3">{type.desc}</p>

                {files[type.key] ? (
                  <div className="flex items-center justify-center space-x-2 text-green-600">
                    <CheckCircle className="w-5 h-5" />
                    <span className="text-sm font-medium truncate max-w-[150px]">
                      {files[type.key].name}
                    </span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-2 text-gray-400">
                    <Upload className="w-5 h-5" />
                    <span className="text-sm">Click to upload</span>
                  </div>
                )}
              </div>
            </label>
          </motion.div>
        ))}
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center space-x-3 text-red-700"
        >
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </motion.div>
      )}

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-center"
      >
        <motion.button
          whileHover={allFilesUploaded ? { scale: 1.05 } : {}}
          whileTap={allFilesUploaded ? { scale: 0.95 } : {}}
          onClick={onAnalyze}
          disabled={!allFilesUploaded}
          className={`px-12 py-4 rounded-full font-bold text-lg shadow-xl transition-all flex items-center space-x-3 mx-auto ${
            allFilesUploaded
              ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:shadow-2xl hover:shadow-purple-500/50"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          <Play className="w-6 h-6" />
          <span>Run Autopsy Analysis</span>
        </motion.button>
      </motion.div>

      <div className="mt-12 p-6 bg-blue-50 rounded-2xl border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
          <span className="mr-2">💡</span> Quick Tips
        </h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>• All three files must have the same column structure</li>
          <li>• CSV files should be properly formatted with headers</li>
          <li>
            • Ensure your production data represents before/after failure
            periods
          </li>
          <li>• Analysis typically completes in 10-30 seconds</li>
        </ul>
      </div>
    </div>
  );
}

export default FileUpload;
