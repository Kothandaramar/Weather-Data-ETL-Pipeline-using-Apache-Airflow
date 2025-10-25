# Save the README content to a text file

readme_content = """# 🌦️ Weather Data ETL Pipeline using Apache Airflow & Python

## 📘 Overview
This project implements a complete **ETL (Extract, Transform, Load)** data pipeline using **Python** and **Apache Airflow**, designed to automate the collection and storage of **real-time weather data** from the **OpenWeather API** for major **Indian cities**.  

The pipeline extracts live data, performs feature engineering and transformations, and loads the cleaned data into a **MySQL Data Warehouse** for analysis, visualization, or downstream processing.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Workflow Orchestration** | Apache Airflow |
| **Programming Language** | Python |
| **Data Source** | OpenWeather API |
| **Database** | MySQL |
| **Libraries Used** | requests, pandas, mysql-connector, sqlalchemy |
| **Storage Output** | MySQL Tables + CSV Backup |

---

## 🧩 Project Architecture

                ┌──────────────────────────────┐
                │        Apache Airflow         │
                │   (Scheduler & Orchestrator)  │
                └──────────────┬────────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │          Extraction           │
                │  → Fetch data from OpenWeather│
                │    API for Indian cities      │
                └──────────────┬────────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │         Transformation        │
                │  → Clean, convert, derive new  │
                │    metrics (temp range, etc.)  │
                └──────────────┬────────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │            Load              │
                │  → Store into MySQL tables:   │
                │    city & weather_fact        │
                └──────────────────────────────┘

---

## 🏗️ Project Structure

Weather-Data-ETL-Pipeline-using-Apache-Airflow/
│
├── dags/
│   └── weather_dag.py                 # Airflow DAG definition
│
├── etl/
│   └── etl_pipeline.py                # ETL class (extraction, transformation, loading)
│
├── config/
│   ├── api_config.json                # API key and URL
│   └── db_config.json                 # MySQL credentials
│
├── Indian_City_Weather.csv            # Output CSV (optional local backup)
│
├── requirements.txt                   # Python dependencies
│
└── README.md

---

## ⚙️ Workflow Explanation

### 1️⃣ Extraction Phase
Fetches real-time weather data for each city from OpenWeather API, normalizes it into structured form, and stores a CSV backup.

### 2️⃣ Transformation Phase
Performs feature engineering and conversions (°C→°F, hPa→atm), fills missing values, and adds new columns like 'temp_range', 'humidity_category', 'pressure_category'petc.

### 3️⃣ Loading Phase
Inserts data into MySQL tables (`city`, `weather_fact`) with foreign key mapping.

---

## 🚀 Setup & Execution

1️⃣ Clone Repository
git clone https://github.com/<your-username>/Weather-Data-ETL-Pipeline-using-Apache-Airflow.git

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\\Scripts\\activate       # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Files
- Add API key in config/api_config.json
- Add MySQL credentials in config/db_config.json

5️⃣ Initialize and Start Airflow
airflow db init
airflow webserver -p 8080
airflow scheduler

6️⃣ Trigger the DAG
Open http://localhost:8080 and start the DAG.

---

## 🧾 Future Enhancements
- Integrate Airflow Sensors for data validation  
- Add AWS S3 or Snowflake as warehouse  
- Build Streamlit dashboard for visualization  
- Implement incremental loading

---

## 👨‍💻 Author
**Kothandaramar Sivakumar**  
📧 skramar1999@gmail.com

---

## 🪪 License
Licensed under the MIT License.
"""
