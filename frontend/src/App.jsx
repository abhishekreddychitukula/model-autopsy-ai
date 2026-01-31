import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import LoadingScreen from "./components/LoadingScreen";
import Dashboard from "./components/Dashboard";
import LandingHero from "./components/LandingHero";
import { API_URL } from "./config";

function App() {
  const [files, setFiles] = useState({
    train: null,
    prod_old: null,
    prod_new: null,
  });
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [showUpload, setShowUpload] = useState(false);

  const handleFilesChange = (newFiles) => {
    setFiles(newFiles);
  };

  const handleAnalyze = async () => {
    if (!files.train || !files.prod_old || !files.prod_new) {
      setError("Please upload all three CSV files");
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("train", files.train);
    formData.append("prod_old", files.prod_old);
    formData.append("prod_new", files.prod_new);

    console.log("Uploading files:", {
      train: files.train.name,
      prod_old: files.prod_old.name,
      prod_new: files.prod_new.name,
    });
    console.log("🔗 Using API URL:", API_URL);

    try {
      const fullUrl = `${API_URL}/run-autopsy`;
      console.log("📡 Fetching:", fullUrl);
      
      const response = await fetch(fullUrl, {
        method: "POST",
        body: formData,
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error("Error response:", errorData);
        
        // Better error message with debugging info
        let errorMessage = errorData.detail || errorData.error || "Analysis failed";
        
        // Add helpful context for common errors
        if (response.status === 404) {
          errorMessage = `Backend not found. Check that:\n1. Backend URL is correct: ${API_URL}\n2. Backend is deployed and running\n3. VITE_API_URL is set in deployment`;
        } else if (response.status === 500) {
          errorMessage = `Server error: ${errorMessage}\n\nThis might be:\n- Column mismatch in CSV files\n- Missing GROQ_API_KEY\n- Backend error (check backend logs)`;
        } else if (response.status === 0 || !response.status) {
          errorMessage = `Cannot reach backend at ${API_URL}\n\nCheck:\n1. Backend is deployed and running\n2. CORS is enabled\n3. URL is correct`;
        }
        
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log("✅ Analysis complete:", data);
      setReport(data);
    } catch (err) {
      console.error("❌ Error:", err);
      
      // Network error (can't reach server)
      if (err.message.includes('Failed to fetch') || err.name === 'TypeError') {
        setError(
          `Cannot connect to backend at ${API_URL}\n\n` +
          `Possible issues:\n` +
          `1. Backend is not deployed or not running\n` +
          `2. Wrong backend URL (check config.js or VITE_API_URL)\n` +
          `3. CORS is blocking the request\n\n` +
          `Current API URL: ${API_URL}`
        );
      } else {
        setError(err.message || "Failed to analyze model. Check console for details.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFiles({
      train: null,
      prod_old: null,
      prod_new: null,
    });
    setReport(null);
    setError(null);
    setShowUpload(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      <Header onReset={handleReset} hasReport={!!report} />

      <main className="container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {!showUpload && !report && (
            <LandingHero onGetStarted={() => setShowUpload(true)} />
          )}

          {showUpload && !loading && !report && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <FileUpload
                files={files}
                onFilesChange={handleFilesChange}
                onAnalyze={handleAnalyze}
                error={error}
              />
            </motion.div>
          )}

          {loading && <LoadingScreen />}

          {report && !loading && (
            <Dashboard report={report} onNewAnalysis={handleReset} />
          )}
        </AnimatePresence>
      </main>

      {/* Floating background elements */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
        <div
          className="absolute top-40 right-10 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"
          style={{ animationDelay: "2s" }}
        ></div>
        <div
          className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"
          style={{ animationDelay: "4s" }}
        ></div>
      </div>
    </div>
  );
}

export default App;
