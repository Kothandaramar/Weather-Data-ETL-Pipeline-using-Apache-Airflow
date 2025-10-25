from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime as dt
from Scripts.etl import ETL
from airflow.models import Variable
import pandas as pd

# get sensitive data from Airflow variables
API_KEY = Variable.get("API_KEY")
DB_PASSWORD = Variable.get("DB_PASSWORD")

# create etl instance
etl = ETL(
    api_key=API_KEY,
    db_config={
        "user": "root",
        "password": DB_PASSWORD,
        "host": "127.0.0.1",  
        "port": 3306,
        "database": "airflow_projects"
    },
    api_url="https://api.openweathermap.org/data/2.5/weather",
    cities=["Chennai", "Coimbatore", "Hyderabad", "Mumbai", "Delhi","Bangalore", "Kolkata", "Ahmedabad", "Pune", "Jaipur", "Surat"]
)

# Functions for tasks
def extract_task(**kwargs) : 
    df = etl.extract()
    kwargs['ti'].xcom_push(key = 'weather_data' , value = df.to_json())

def transform_task(**kwargs) :
    ti = kwargs['ti']
    df_json = ti.xcom_pull(key = 'weather_data' , task_ids = 'extract')
    df = pd.read_json(df_json)
    transformed_df = etl.transform(df)
    ti.xcom_push(key = 'transformed_weather_data' , value = transformed_df.to_json())


def load_task(**kwargs) : 
    ti = kwargs['ti']
    df_json = ti.xcom_pull(key = 'transformed_weather_data' , task_ids = 'transform')
    df = pd.read_json(df_json)
    etl.load(df)
    

# Default arguments
def_args = {
    'owner' : 'airflow',
    'start_date' : dt(2025, 1, 1) ,
    'retries' : 1 
}

# Define the DAG
with DAG("weather_data_pipeline" , default_args = def_args , catchup = False) as dag :
    
    start = EmptyOperator(task_id = "start")
    
    extract = PythonOperator(
        task_id = "extract" , 
        python_callable = extract_task 
    )
    
    transform = PythonOperator(
        task_id = "transform" , 
        python_callable = transform_task     
    )

    load = PythonOperator(
        task_id = "load" , 
        python_callable = load_task
    )

    end = EmptyOperator(task_id = "end")
    
# Dependencies
start >> extract >> transform >> load >> end
