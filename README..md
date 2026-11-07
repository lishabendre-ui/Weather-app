# 🌤️ Weather Data Pipeline & Dashboard

An end-to-end, automated data pipeline that extracts daily weather forecasts for multiple global cities from the Open-Meteo API, cleans and validates the data using **Python (pandas)**, loads it idempotently into a **SQLite** relational database, and presents actionable insights through an interactive **Streamlit** dashboard.

---

## 🏗️ Architecture & Data Flow

```text
[Open-Meteo API] 
       │ (HTTP GET)
       ▼
 [extract.py] ──> Saves untouched raw JSON to data/raw/weather_raw.json (Bronze Layer)
       │
       ▼
[transform.py] ──> Cleans data, standardizes types, validates missing values (Silver Layer)
       │
       ▼
  [load.py]   ──> Idempotent insert into SQLite relational tables (Gold Layer)
       │
       ├───> [analyze.py]  (SQL analytical queries & summaries)
       └───> [app.py]      (Interactive Streamlit dashboard)
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.15+
- **Data Ingestion:** `requests` (Open-Meteo REST API)
- **Data Transformation:** `pandas`
- **Storage / Database:** SQLite (`sqlite3`)
- **Visualization:** Streamlit
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```text
Weather-app/
├── data/
│   ├── raw/
│   │   └── weather_raw.json   # Untouched API JSON responses (git-ignored)
│   └── weather.db             # SQLite relational database (git-ignored)
├── extract.py                 # Fetches forecast for 5 cities from Open-Meteo API
├── transform.py               # Unpacks, validates, and cleans raw data using pandas
├── create_db.py               # Initializes SQLite database and table schemas
├── load.py                    # Inserts records into SQLite without duplicates
├── analyze.py                 # Runs analytical SQL queries (hottest days, averages)
├── app.py                     # Interactive Streamlit dashboard with charts
├── main.py                    # Master orchestrator script running end-to-end pipeline
├── requirements.txt           # Project dependencies
├── .gitignore                 # Filters out virtual environment and data files
└── README.md                  # Project documentation
```

---

## 🗄️ Database Schema

The SQLite database (`data/weather.db`) uses a normalized relational schema with constraints:

### `cities` (Dimension Table)
- `city_id` (INTEGER, Primary Key, Auto-increment)
- `city_name` (TEXT, Unique, Not Null)
- `latitude` (REAL, Not Null)
- `longitude` (REAL, Not Null)

### `weather_daily` (Fact Table)
- `record_id` (INTEGER, Primary Key, Auto-increment)
- `city_id` (INTEGER, Foreign Key referencing `cities(city_id)`)
- `date` (TEXT, Not Null)
- `temp_max_c` (REAL, Not Null)
- `temp_min_c` (REAL, Not Null)
- `precipitation_mm` (REAL, Not Null)
- **Constraint:** `UNIQUE (city_id, date)` ensures idempotent loads.

---

## 🚀 How to Set Up and Run

### 1. Clone the repository
```bash
git clone https://github.com/lishabendre-ui/Weather-app.git
cd Weather-app
```

### 2. Set up virtual environment & install requirements
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the complete data pipeline end-to-end
```bash
python3 main.py
```

### 4. Run SQL analytical queries in terminal
```bash
python3 analyze.py
```

### 5. Launch the Streamlit dashboard
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.
