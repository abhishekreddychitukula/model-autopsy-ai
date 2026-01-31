# 🚀 HACKATHON DEMO GUIDE

## Quick Demo Setup (5 minutes)

### Step 1: Install & Run

```bash
# Windows
run.bat

# Mac/Linux
chmod +x run.sh
./run.sh
```

### Step 2: Generate Sample Data

```bash
python generate_sample_data.py
```

This creates three CSV files with intentional drift:

- `sample_train.csv` - Baseline
- `sample_prod_old.csv` - Pre-failure
- `sample_prod_new.csv` - Post-failure (with drift)

### Step 3: Run Autopsy

1. Open http://127.0.0.1:8000/docs
2. Navigate to `/run-autopsy` endpoint
3. Click "Try it out"
4. Upload the three sample CSV files
5. Click "Execute"
6. **Watch the magic happen! ✨**

## 🎯 What to Highlight to Judges

### 1. The Problem (30 seconds)

_"ML models fail silently in production. Current tools show metrics dropping but don't explain WHY. Engineers spend days debugging."_

### 2. The Solution (30 seconds)

_"Model Autopsy AI automatically diagnoses failures by:_

- _Detecting which features drifted_
- _Measuring their impact_
- _Explaining the root cause in plain English"_

### 3. Technical Innovation (60 seconds)

Show the report sections:

#### a) Drift Detection

```json
{
  "feature": "income",
  "method": "KS-Test",
  "drift_score": 0.42,
  "severity": "High"
}
```

_"We use industry-standard statistical tests: KS-Test for numerical, PSI for categorical"_

#### b) Impact Analysis

```json
{
  "feature": "income",
  "impact_score": 0.38,
  "impact_level": "High"
}
```

_"We don't just detect drift - we measure business impact"_

#### c) LLM Diagnosis

_"The system converts statistics into actionable insights using GPT-4"_

Show the diagnosis section with plain-English explanation.

### 4. The WOW Factor (30 seconds)

**Critical Features Correlation:**

```json
{
  "critical_features": ["income", "credit_score"],
  "explanation": "These features BOTH drifted AND have high impact"
}
```

_"We establish causality, not just correlation. We tell you exactly which features caused the failure."_

### 5. Production Ready (30 seconds)

Show:

- ✅ Data validation (catches pipeline failures)
- ✅ Error handling
- ✅ API documentation (Swagger)
- ✅ Extensible architecture
- ✅ Works with OR without LLM (rule-based fallback)

## 📊 Expected Results from Sample Data

You should see:

1. **8 features with drift**
2. **3 critical features** (high drift + high impact):
   - `income` - Mean shift
   - `credit_score` - Distribution change
   - `age` - Variance increase
3. **New categorical values detected**:
   - `location`: 'remote' (new)
   - `education`: 'phd' (new)
4. **Severity**: "HIGH - Action recommended soon"
5. **LLM Diagnosis** explaining the root cause

## 🎬 Demo Script (3 minutes)

### Minute 1: Problem Setup

1. Open slides/explain problem
2. Show sample data files
3. Explain the scenario: "Loan approval model suddenly degrading"

### Minute 2: Run Autopsy

1. Navigate to Swagger UI
2. Upload files
3. Execute autopsy
4. **While waiting, explain the pipeline:**
   - "First, data validation..."
   - "Then drift detection using KS-Test..."
   - "Impact analysis..."
   - "LLM generates diagnosis..."

### Minute 3: Results Walkthrough

1. **Executive Summary**: Point out severity
2. **Drift Leaderboard**: Show top drifted features
3. **Critical Features**: "These are your root causes"
4. **LLM Diagnosis**: Read key sections
5. **Recommendations**: Show actionable next steps

## 💡 Talking Points

### For Technical Judges:

- "Uses industry-standard drift detection: KS-Test (p<0.05), PSI (banking standard)"
- "Modular architecture - easy to extend with new detection methods"
- "Works without model access using proxy metrics"
- "Can integrate SHAP for model-based impact analysis"

### For Business Judges:

- "Reduces debugging time from days to minutes"
- "Prevents revenue loss from model failures"
- "Actionable insights in plain English"
- "Automated root cause analysis"

### For Everyone:

- "This is a real problem costing companies millions"
- "No existing tool provides automated diagnosis"
- "We combine ML, statistics, and AI to solve it"

## 🔥 Impressive Features to Call Out

1. **Automatic Pipeline Failure Detection**
   - Catches new categorical values
   - Detects schema changes
   - Identifies null explosions

2. **Statistical Rigor**
   - KS-Test: Non-parametric, widely accepted
   - PSI: Banking industry standard
   - Clear severity thresholds

3. **LLM Integration**
   - Converts numbers to insights
   - Generates actionable recommendations
   - Explains causality

4. **Timeline Reconstruction**
   - "We don't just say what failed, we show WHEN"
   - Establishes causal relationships
   - Identifies first feature to drift

5. **Production Ready**
   - Full API documentation
   - Error handling
   - Extensible design
   - Works offline (LLM optional)

## 🎪 Backup Demo (If Live Demo Fails)

Have screenshots ready showing:

1. Swagger UI with file upload
2. JSON response with results
3. Key sections of diagnosis

**Or use pre-generated report:**

```bash
# Run autopsy and save results
curl -X POST http://127.0.0.1:8000/run-autopsy \
  -F "train=@sample_train.csv" \
  -F "prod_old=@sample_prod_old.csv" \
  -F "prod_new=@sample_prod_new.csv" \
  > demo_report.json
```

## ❓ Anticipated Questions

**Q: "What if I don't have the old production data?"**
A: "The system works with just train + new production. Old data helps with timeline analysis but isn't required."

**Q: "Does this work with any ML model?"**
A: "Yes! It's model-agnostic. Analyzes data drift regardless of model type."

**Q: "What about false positives?"**
A: "We use established statistical thresholds (p<0.05, PSI>0.25). These are industry standards with low false positive rates."

**Q: "How do you handle feature importance without the model?"**
A: "We use proxy metrics: distribution shifts, correlation changes. If model is available, we can integrate SHAP."

**Q: "Can this run in real-time?"**
A: "Current version is batch analysis. Real-time streaming drift detection is on our roadmap."

**Q: "What's the cost of running this?"**
A: "Minimal. Statistical tests are fast. LLM calls are optional (falls back to rules). Could process thousands of features in seconds."

## 🏆 Winning Points

1. **Solves Real Problem**: Not a toy project - addresses actual pain point
2. **Technical Depth**: Proper statistical methods, not hand-waving
3. **Innovation**: LLM-powered diagnosis is novel
4. **Completeness**: End-to-end solution with API, docs, examples
5. **Production Ready**: Error handling, validation, extensibility

## 📸 Screenshot Checklist

Before demo, take screenshots of:

- [ ] Swagger UI
- [ ] Sample report JSON
- [ ] Drift leaderboard
- [ ] LLM diagnosis section
- [ ] Health check endpoint

## 🎯 Final Tips

1. **Practice the demo** - Know exactly where to click
2. **Have backup plan** - Pre-generated results ready
3. **Tell a story** - "Imagine you're a data scientist, your model just failed..."
4. **Be confident** - This is a GOOD solution to a REAL problem
5. **Show passion** - You built something useful!

---

**Good luck! You've got this! 🚀**
