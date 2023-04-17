import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from sqlalchemy import create_engine

from airflow.utils.dates import days_ago
from spotify_etl import spotify_etl
import psycopg2

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(2023,4,14),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}

dag = DAG(
    'spotify_final_dag',
    default_args=default_args,
    description='Spotify ETL process 1-min',
    schedule_interval=dt.timedelta(minutes=50),
)

def ETL():
    print("started")
    df=spotify_etl()
    #print(df)
    conn = BaseHook.get_connection('postgre_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql('top_songs', engine, if_exists='replace')

with dag:    
    create_table = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id = 'postgre_sql',
        sql = """
            CREATE TABLE IF NOT EXISTS top_songs (
            id SERIAL PRIMARY KEY,
            song_date VARCHAR(200),
            song_name VARCHAR(200),
            artist_name VARCHAR(200)
            );"""
    )

    run_etl = PythonOperator(
        task_id = 'spotify_etl_final',
        python_callable = ETL,
        dag = dag,
    )

    create_table >> run_etl