# Model Autopsy AI - Frontend

Beautiful React frontend for the Model Autopsy AI application.

## 🚀 Quick Start

### Install Dependencies

```bash
cd frontend
npm install
```

### Start Development Server

```bash
npm run dev
```

The app will open at http://localhost:3000

### Build for Production

```bash
npm run build
```

## 🎨 Features

- ✨ Modern, gradient-based design
- 📊 Interactive charts (Recharts)
- 🎭 Smooth animations (Framer Motion)
- 🎯 Responsive layout (Tailwind CSS)
- ⚡ Fast development (Vite)
- 🔄 Real-time API integration

## 🛠️ Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Lucide React** - Icons
- **Axios** - HTTP client

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── charts/
│   │   │   ├── DriftChart.jsx
│   │   │   ├── ImpactChart.jsx
│   │   │   └── CorrelationChart.jsx
│   │   ├── Header.jsx
│   │   ├── LandingHero.jsx
│   │   ├── FileUpload.jsx
│   │   ├── LoadingScreen.jsx
│   │   ├── Dashboard.jsx
│   │   ├── StatCard.jsx
│   │   └── DiagnosisSection.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## 🎯 Usage

1. **Landing Page**: Click "Start Diagnosis"
2. **Upload Files**: Drag & drop or click to upload 3 CSV files
3. **Run Analysis**: Click "Run Autopsy Analysis"
4. **View Results**: Explore drift charts, impact analysis, and AI diagnosis

## 🌈 Color Scheme

- **Primary**: Purple to Blue gradient
- **Danger**: Red (drift/critical)
- **Warning**: Orange (moderate severity)
- **Success**: Green (low severity)

## 🔧 Configuration

The app proxies API requests to `http://127.0.0.1:8000` automatically.

To change the backend URL, edit `vite.config.js`.

## 📝 Notes

- Ensure the FastAPI backend is running on port 8000
- For production, build the app and serve the `dist` folder
- All charts are responsive and mobile-friendly
