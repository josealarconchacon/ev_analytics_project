# EV Analytics Project

This project analyzes electric vehicle population data using SQL and Python with an interactive web dashboard.

## Features

- Top EV Manufacturers (SQL + visualization)
- EV Growth Over Years
- Geographic distribution analysis
- Performance metrics and range analysis
- Interactive web dashboard with Streamlit
- Modular, scalable file structure
- SQLite database for SQL querying

## How to Run

### Launch Interactive Web Dashboard

```bash
# Method 1: Using the launcher script
python3 run_dashboard.py

# Method 2: Direct streamlit command
cd src
streamlit run dashboard.py

# Method 3: Using the module
python3 -c "from src import run_web_dashboard; run_web_dashboard()"
```

## Dashboard Features

The interactive web dashboard includes:

- 📈 **Overview Tab**: Key metrics and growth trends
- 🏭 **Manufacturers Tab**: Manufacturer analysis and range comparisons
- 🗺️ **Geographic Tab**: County and city distribution maps
- 🔋 **Performance Tab**: EV types and range distribution
- 📊 **Detailed Analysis Tab**: Raw data tables and download options

## Setup Instructions

1. Install dependencies:

```bash
# Install clean requirements (recommended)
pip install -r requirements_clean.txt

# Or install only essential packages manually
pip install pandas numpy matplotlib seaborn plotly streamlit
```

2. Ensure your data file is in the correct location:

```
data/ev_data.csv
```

3. Run the dashboard:

```bash
python3 run_dashboard.py
```

4. Open your browser and navigate to:

```
http://localhost:8501
```
