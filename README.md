# 🔬 Model Autopsy AI

**Automated Root Cause Analysis for ML Model Failure**

A comprehensive ML model debugging system that automatically diagnoses model failures by detecting data drift, analyzing feature impact, and generating actionable insights using LLM-powered analysis.

## 🎯 Problem Statement

Machine learning models fail silently in production due to data drift and feature instability. Current monitoring systems detect performance degradation but lack automated root-cause analysis and explainability. This leads to delayed diagnosis, costly downtime, and unreliable AI systems.

**Model Autopsy AI** solves this by automatically:

- ✅ Identifying which features changed
- ✅ Determining when they changed
- ✅ Measuring their impact on the model
- ✅ Explaining what to do next in human language

## 🏗️ Architecture

```
┌────────────┐
│ CSV Upload │
└─────┬──────┘
      ↓
┌───────────────┐
│ Data Validator│
└─────┬─────────┘
      ↓
┌─────────────────────────┐
│ Drift Detection Engine  │
│ (KS-Test, PSI)         │
└─────┬──────────────────┘
      ↓
┌─────────────────────────┐
│ Feature Impact Analyzer │
│ (Proxy Metrics / SHAP)  │
└─────┬──────────────────┘
      ↓
┌─────────────────────────┐
│ Drift Timeline Builder  │
└─────┬──────────────────┘
      ↓
┌─────────────────────────┐
│ LLM Diagnosis Engine    │
│ (OpenAI GPT-4)         │
└─────┬──────────────────┘
      ↓
┌─────────────────────────┐
│ Comprehensive Report    │
└─────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
cd model-autopsy-ai

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key (optional)
```

### Running the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Server will start at http://127.0.0.1:8000
```

### Access the API

- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## 📊 Usage

### Required Data Files

Prepare three CSV files:

1. **train.csv** - Training/baseline data
2. **prod_old.csv** - Production data before failure
3. **prod_new.csv** - Production data after failure

### Running an Autopsy

#### Option 1: Using the API Documentation (Recommended for Demo)

1. Navigate to http://127.0.0.1:8000/docs
2. Click on `/run-autopsy` endpoint
3. Click "Try it out"
4. Upload your three CSV files
5. Click "Execute"
6. View the comprehensive autopsy report

#### Option 2: Using cURL

```bash
curl -X POST "http://127.0.0.1:8000/run-autopsy" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "train=@train.csv" \
  -F "prod_old=@prod_old.csv" \
  -F "prod_new=@prod_new.csv"
```

#### Option 3: Using Python

```python
import requests

files = {
    'train': open('train.csv', 'rb'),
    'prod_old': open('prod_old.csv', 'rb'),
    'prod_new': open('prod_new.csv', 'rb')
}

response = requests.post('http://127.0.0.1:8000/run-autopsy', files=files)
report = response.json()

print(report['diagnosis']['full_diagnosis'])
```

## 🔍 What You Get

### Autopsy Report Includes:

1. **Executive Summary**
   - Overall severity assessment
   - Critical features count
   - Business impact analysis

2. **Drift Analysis**
   - Features with distribution drift
   - Drift scores and severity levels
   - Statistical test results (KS-Test, PSI)

3. **Impact Analysis**
   - Feature impact scores
   - High-impact feature identification
   - Distribution metrics

4. **Timeline Reconstruction**
   - Chronological failure analysis
   - Critical event identification
   - Drift-to-impact correlation

5. **LLM-Powered Diagnosis**
   - Root cause explanation in plain English
   - Mechanism of failure
   - Immediate action items
   - Long-term preventive measures

## 🧪 Example Report Structure

```json
{
  "executive_summary": {
    "summary": "Model failure due to severe drift in 3 critical features",
    "severity": "CRITICAL - Immediate action required",
    "business_impact": "HIGH - Immediate business impact likely"
  },
  "drift_analysis": {
    "summary": {
      "total_features_analyzed": 15,
      "drifted_features_count": 8,
      "severe_drift_count": 3
    },
    "drift_leaderboard": [...]
  },
  "diagnosis": {
    "full_diagnosis": "Comprehensive analysis with actionable recommendations..."
  }
}
```

## 🎓 Technical Deep Dive

### Drift Detection Methods

#### Numerical Features: KS-Test (Kolmogorov-Smirnov)

- Non-parametric test
- Compares cumulative distributions
- p-value < 0.05 indicates significant drift

#### Categorical Features: PSI (Population Stability Index)

- Industry standard in banking/risk models
- Thresholds:
  - PSI < 0.1: No drift
  - 0.1 ≤ PSI < 0.25: Moderate drift
  - PSI ≥ 0.25: Severe drift (retrain recommended)

### Impact Analysis

**Proxy Impact Metrics** (works without model):

- Mean shift magnitude
- Variance changes
- Distribution overlap reduction

**SHAP Analysis** (if model available):

- Feature importance via SHAP values
- Individual prediction explanations

### LLM Integration

The system uses GPT-4 (or falls back to rule-based analysis) to:

- Convert statistical results into human-readable insights
- Provide contextual recommendations
- Explain causal relationships
- Generate actionable next steps

## 📁 Project Structure

```
model-autopsy-ai/
│
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Configuration
│   │
│   ├── api/
│   │   └── routes.py            # API endpoints
│   │
│   ├── services/
│   │   ├── data_loader.py       # CSV validation
│   │   ├── drift_detection.py   # KS-Test, PSI
│   │   ├── impact_analysis.py   # Impact scoring
│   │   ├── timeline.py          # Timeline builder
│   │   └── llm_diagnosis.py     # LLM integration
│   │
│   ├── models/
│   │   └── schemas.py           # Pydantic models
│   │
│   ├── utils/
│   │   └── stats.py             # Statistical utilities
│   │
│   └── reports/
│       └── report_builder.py    # Report generation
│
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

**Note**: The system works without an OpenAI API key by falling back to rule-based diagnosis.

## 🎯 Hackathon Demo Tips

### Impressive Features to Highlight:

1. **Automated Root Cause Analysis** - No manual debugging needed
2. **Statistical Rigor** - Industry-standard tests (KS, PSI)
3. **LLM Integration** - Human-readable explanations
4. **Timeline Reconstruction** - Establishes causality, not just correlation
5. **Production-Ready** - Validation, error handling, extensibility

### Demo Flow:

1. Show health check endpoint
2. Upload sample CSVs via Swagger UI
3. Highlight drift detection results
4. Show LLM diagnosis section
5. Explain actionable recommendations

### Talking Points:

- "This solves a real problem: ML models fail silently in production"
- "Current tools show metrics but don't explain WHY"
- "We automatically identify root cause and provide human-readable explanations"
- "Uses industry-standard drift detection methods"
- "LLM converts statistics into actionable business insights"

## 🚦 API Endpoints

### `POST /run-autopsy`

Run complete autopsy analysis

**Input**:

- `train` (file): Training data CSV
- `prod_old` (file): Production data before failure
- `prod_new` (file): Production data after failure

**Output**: Comprehensive autopsy report (JSON)

### `POST /analyze-drift`

Quick drift analysis without full autopsy

**Input**:

- `train` (file): Training data
- `production` (file): Production data

**Output**: Drift detection results only

### `GET /health`

Health check endpoint

## 🔬 Statistical Methods Explained

### Why KS-Test for Numerical Features?

- **Non-parametric**: No distribution assumptions
- **Sensitive**: Detects shape, location, and scale changes
- **Interpretable**: Clear p-value threshold (0.05)

### Why PSI for Categorical Features?

- **Industry Standard**: Used in banking, credit risk
- **Interpretable Scale**: Clear severity thresholds
- **Practical**: Directly applicable to business contexts

## 🛠️ Extending the System

### Adding New Drift Detection Methods

```python
# In drift_detection.py
def _detect_custom_drift(train, prod, feature):
    # Your custom drift detection logic
    return drift_result
```

### Adding SHAP Analysis

When you have a trained model:

```python
from app.services.impact_analysis import calculate_shap_impact

impact = calculate_shap_impact(model, train_df, prod_df)
```

### Custom LLM Providers

Replace OpenAI with Gemini or other providers in `llm_diagnosis.py`

## 📈 Future Enhancements

- [ ] Real-time streaming drift detection
- [ ] Multi-model comparison
- [ ] Automated retraining triggers
- [ ] Integration with MLOps platforms
- [ ] PDF report generation
- [ ] Email alerting
- [ ] Dashboard frontend (React)

## 🤝 Contributing

This is a hackathon project. Feel free to:

- Report issues
- Suggest enhancements
- Submit pull requests

## 📄 License

MIT License - Feel free to use for your projects

## 🏆 Credits

Built for [Your Hackathon Name]

**Team Members**: [Your Names]

**Technologies Used**:

- FastAPI - Web framework
- Pandas/NumPy - Data processing
- SciPy - Statistical tests
- SHAP - Explainability
- OpenAI GPT-4 - LLM diagnosis

---

## 🎬 Quick Demo Script

```bash
# 1. Start server
uvicorn app.main:app --reload

# 2. In browser: http://127.0.0.1:8000/docs

# 3. Upload CSVs and run autopsy

# 4. Show results highlighting:
#    - Drift leaderboard
#    - Critical features
#    - LLM diagnosis
#    - Actionable recommendations
```

---

**Questions?** Open an issue or contact the team!

**Good luck with your hackathon! 🚀**
