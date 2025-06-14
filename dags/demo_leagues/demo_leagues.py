"""
*************************************************************
Author = @lexbonella -- https://github.com/alexbonella      *
Date = '22/09/2022'                                         *
Description = Extracting Data from Multiple Football League *
*************************************************************
"""


import json
from datetime import datetime, timedelta
import os
import logging
import airflow
from airflow.models import Variable
from airflow import models
from airflow.models import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import snowflake.connector as sf
import pandas as pd
import time
import random
import os
from utils import get_data,data_processing
from datetime import datetime




default_arguments = {   'owner': 'Dhernandez',
                        'email': 'daniher02@gmail.com',
                        'retries':1 ,
                        'retry_delay':timedelta(minutes=5)}


params_info = Variable.get("feature_info", deserialize_json=True)
df = pd.read_csv('/usr/local/airflow/df_ligas.csv')
df_team = pd.read_csv('/usr/local/airflow/team_table.csv')

def extract_info(df ,df_team ,**kwargs):

    df_data = data_processing(df) # buscar procesar por liga individual

    df_final = pd.merge(df_data,df_team,how='inner',on='EQUIPO')
    df_final = df_final[['ID_TEAM','EQUIPO', 'J', 'G', 'E', 'P', 'GF', 'GC', 'DIF', 'PTS', 'LIGA',
        'CREATED_AT']]

    df_final.to_csv('./premier_positions.csv',index=False)
    
def extract_info_by_liga(df_team,liga, url, **kwargs):
    
    print(f"🔄 PROCESANDO LIGA: {liga}")
    print(f"🌐 URL: {url}")
    print(f"📅 Timestamp: {datetime.now()}")

    df_data = get_data(url,liga) # buscar procesar por liga individual

    df_final = pd.merge(df_data,df_team,how='inner',on='EQUIPO')
    df_final = df_final[['ID_TEAM','EQUIPO', 'J', 'G', 'E', 'P', 'GF', 'GC', 'DIF', 'PTS', 'LIGA',
        'CREATED_AT']]

    df_final.to_csv(f'./premier_positions.csv',index=False)


with DAG('FOOTBAL_LEAGUES',
         default_args=default_arguments,
         description='Extracting Data Footbal League' ,
         start_date = datetime(2025, 6, 11),
         schedule  = None, # en formato cron, None si no se quiere programar
         tags=['tabla_espn'],
         catchup=False) as dag :
    
         grupos = []
    
         for index, row in df.iterrows(): 
            liga = row['LIGA']
            url = row['URL']

            with TaskGroup(group_id=f'liga_{liga.lower()}') as grupo:

                extract_task = PythonOperator(
                    task_id=f'extract_{liga.lower()}',
                    python_callable=extract_info_by_liga,
                    op_kwargs={"df_team": df_team, "liga": liga, "url": url}
                )
                
                validate_task = PythonOperator(
                    task_id='validate_data',
                    python_callable=lambda liga=liga: print(f"Validando {liga}")
                )
                
                extract_task >> validate_task  # Secuencia dentro del grupo

            grupos.append(grupo)

        #  extract_data = PythonOperator(task_id='EXTRACT_FOTBALL_DATA',
        #                             # provide_context=True,
        #                             python_callable=extract_info,
        #                             op_kwargs={"df":df,"df_team":df_team})

         upload_stage = SQLExecuteQueryOperator(

                    task_id='upload_data_stage',
                    sql='./queries/upload_stage.sql',
                    conn_id='demo_snow_new',
                    params=params_info
                    )
         ingest_table = SQLExecuteQueryOperator(

                    task_id='ingest_table',
                    sql='./queries/upload_table.sql',
                    conn_id='demo_snow_new',
                    params=params_info
                    )

         grupos >>  upload_stage >> ingest_table