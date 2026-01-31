"""Configuration and constants for Model Autopsy AI"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Drift Detection Thresholds
KS_TEST_THRESHOLD = 0.05  # p-value threshold for KS test
PSI_MODERATE_THRESHOLD = 0.1
PSI_SEVERE_THRESHOLD = 0.25

# Impact Analysis
IMPACT_HIGH_THRESHOLD = 0.3
IMPACT_MODERATE_THRESHOLD = 0.1

# Supported column types
NUMERICAL_TYPES = ['int64', 'float64', 'int32', 'float32']
CATEGORICAL_TYPES = ['object', 'category', 'bool']
