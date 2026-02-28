# Baseline Calibration Prototype

A web application that analyzes typing patterns, coding behavior, and cognitive responses to generate a behavioral baseline vector.

## Features

- **Welcome Screen**: Introduction to the calibration process
- **Privacy Notice**: Clear disclosure about data handling
- **Profile Collection**: Gather experience and work habit information
- **Controlled Typing Test**: Measure typing patterns and consistency
- **Adaptive Coding Test**: Multi-stage coding assessment with adaptive difficulty
- **Cognitive Variation Task**: Logical problem-solving measurement
- **Summary Display**: Comprehensive baseline vector visualization

## Tech Stack

### Frontend
- React 18 with Vite
- Dark theme (#0f0f0f background)
- Neon blue accent (#4cc9f0)
- Clean, minimal UI with smooth transitions

### Backend
- Python FastAPI
- CORS enabled for localhost
- In-memory session storage

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- pip

## Installation & Running

### 1. Clone/Download the Project

```bash
cd amd2
```

### 2. Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will run at: http://localhost:8000

### 3. Setup Frontend (in a new terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run at: http://localhost:5173

### 4. Access the Application

Open your browser and navigate to: **http://localhost:5173**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/profile` | POST | Save user profile and calculate experience factor |
| `/typing-metrics` | POST | Process typing test data |
| `/coding-metrics` | POST | Process coding test data |
| `/summary` | GET | Get complete calibration summary |
| `/health` | GET | Health check endpoint |
| `/reset` | POST | Reset session data |

## Metrics Calculated

### Keyboard Metrics
- **mean_ikt**: Mean inter-keystroke time
- **std_ikt**: Standard deviation of inter-keystroke time
- **coefficient_of_variation**: Typing consistency measure
- **correction_rate**: Backspace frequency
- **pause_ratio**: Pauses > 800ms
- **long_pause_ratio**: Pauses > 1500ms
- **typing_speed**: Characters per minute

### Cognitive Profile
- **std_shift_between_stages**: Consistency change across coding stages
- **correction_shift**: Correction rate change across stages
- **latency_shift**: Response time change across stages
- **frustration_index**: Based on long pauses and rewrites
- **load_sensitivity**: Performance variation under cognitive load

## Project Structure

```
amd2/
├── backend/
│   ├── main.py           # FastAPI application with all endpoints
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html        # HTML entry point
│   ├── package.json      # Node dependencies
│   ├── vite.config.js    # Vite configuration
│   └── src/
│       ├── main.jsx      # React entry point
│       ├── App.jsx       # Main application with all screens
│       └── index.css     # Dark theme styles
└── README.md             # This file
```

## Privacy

- **No text content is stored** - only timing patterns
- **No data leaves your device** - runs entirely locally
- **No database** - all data is in-memory during session only
- **No authentication** - prototype mode

## Development Notes

- The application uses in-memory storage; restarting the backend clears all data
- The adaptive coding test adjusts based on performance (correction rate and pause rate)
- Classifications (Stable/Moderate/Variable, Low/Medium/High) are computed server-side

## Troubleshooting

### Backend won't start
- Ensure Python 3.9+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

### Frontend won't start
- Ensure Node.js 18+ is installed
- Run `npm install` in the frontend directory
- Check if port 5173 is available

### CORS errors
- Ensure backend is running on port 8000
- Check that CORS is properly configured (already set in main.py)

## License

This is a prototype for demonstration purposes.
