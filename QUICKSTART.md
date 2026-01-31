# 🚀 QUICK START - Model Autopsy AI

## Fastest Way to Get Started (3 steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Generate Sample Data

```bash
python generate_sample_data.py
```

This creates:

- `sample_train.csv` - Training baseline
- `sample_prod_old.csv` - Production before failure
- `sample_prod_new.csv` - Production after failure (with intentional drift)

### Step 3: Start Server

```bash
# Windows
uvicorn app.main:app --reload

# Or use the convenience script
run.bat  # Windows
./run.sh # Mac/Linux
```

## Test the API

### Option A: Browser (Easiest)

1. Open http://127.0.0.1:8000/docs
2. Try the `/run-autopsy` endpoint
3. Upload the three sample CSV files
4. Click "Execute"
5. View your autopsy report! 🎉

### Option B: Command Line

```bash
# PowerShell
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/run-autopsy" `
  -Method Post `
  -Form @{
    train = Get-Item "sample_train.csv"
    prod_old = Get-Item "sample_prod_old.csv"
    prod_new = Get-Item "sample_prod_new.csv"
  }

$response | ConvertTo-Json -Depth 10
```

## Expected Results

You should see:

- ✅ **8 features** with detected drift
- ✅ **3 critical features** (drift + high impact)
- ✅ **New categorical values** detected
- ✅ **LLM diagnosis** with plain-English explanation
- ✅ **Actionable recommendations**

## API Endpoints

- **Swagger Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health
- **Full Autopsy**: `POST /run-autopsy`
- **Quick Drift**: `POST /analyze-drift`

## Environment Setup (Optional)

For LLM-powered diagnosis (optional but impressive):

1. Copy `.env.example` to `.env`
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

**Note**: System works without API key using rule-based diagnosis.

## Troubleshooting

### "Module not found"

```bash
pip install -r requirements.txt
```

### "Port already in use"

```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

### "File not found"

Make sure you're in the `model-autopsy-ai` directory:

```bash
cd model-autopsy-ai
python generate_sample_data.py
```

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🎯 Check [DEMO_GUIDE.md](DEMO_GUIDE.md) for hackathon demo tips
- 🧪 Try with your own CSV data files

---

**Ready for your hackathon demo! 🏆**
