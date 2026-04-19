from t_tech.invest import Client
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
from Scripts.generate_clients import generate_clients_csv
from sql.sql_insert_data_from_s3 import insert_data_from_s3
import os


# === Глобальные параметры ===
S3_BUCKET = 'airflow-bucket'
S3_KEY_PREFIX = 't-investment'
TOKEN = Variable.get("t-bank_token")
# =======================================================


def get_tinkoff_last_prices(token: str, df: pd.DataFrame) -> pd.DataFrame:
    try:
        with Client(token) as client:
            last_prices = client.market_data.get_last_prices(figi=df['figi'].to_list())
    except Exception as e:
        raise Exception('--> tinkoff api - last price - Ошибка загрузки последней цены.')

    last_prices = pd.DataFrame(last_prices.last_prices)

    return last_prices


def get_stock_price(token:str):

    try:
        print(f"TOKEN: {TOKEN}")
        # Список тикеров
        tickets = ["LKOH","RTKMP","TATNP","SBERP","PLZL","PHOR"]
        with Client(TOKEN) as client:
            shares = client.instruments.shares()
            print(client.users.get_accounts())


        # Получаем список акций
        shares = pd.DataFrame(shares.instruments)
        print("shares")
        print(type(shares))
        print(shares)
        print("-------------------------------------------------")
        # df = shares['ticker'].isin(tickets)
        # df = shares[shares['ticker'].isin(tickets)]
        # print(df)

        # print(get_tinkoff_last_prices(token=TOKEN, df=df))

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"/opt/airflow/dags/Scripts/Temp/{date}.json"
        shares.to_json(path_or_buf=filename, orient='records', indent=4)

        return {"file_name": f"{date}.json"}

    except Exception as e:
        print(f"Ошибка: {e}")


def upload_to_minio_json(**context):
# def upload_to_minio(**context):

    try:

        # Your JSON data
        data = context["ti"].xcom_pull(task_ids="get_stock_price")
        print("data")
        print(f"{data}")
        json_string = json.dumps(data)
        
        print("json_string")
        print(f"{json_string}")

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        execution_date = f"{date}.json"
        s3_key = f"{S3_KEY_PREFIX}/bronze/{execution_date}"


        hook = S3Hook(aws_conn_id='minio_S3')
        hook.load_string(
            string_data=json_string,
            key=s3_key,
            bucket_name=S3_BUCKET,
            replace=True
        )
       
        print(f"Файл {tmp_file_path} успешно загружен в s3://{S3_BUCKET}/{s3_key}")

        return f"s3://{S3_BUCKET}/{s3_key}"

    except Exception as e:
        print(f"Ошибка в работе метода upload_to_minio: {e}")


def upload_to_minio(**context):
    try:
        file_name = context["ti"].xcom_pull(task_ids="get_stock_price")
        print(f"file_name: {file_name}")
        if not file_name:
            print(f"file_name: {file_name}")
            return None
        else:
            print(f"file_name: {file_name}")
        tmp_file_path = f"/opt/airflow/dags/Scripts/Temp/{file_name["file_name"]}"
        execution_date = file_name["file_name"]

        if not tmp_file_path:
            print(f"Файл для даты {execution_date} не был создан. Пропуск загрузки.")
            return

        s3_key = f"{S3_KEY_PREFIX}/bronze/{execution_date}"

        hook = S3Hook(aws_conn_id='minio_S3')
        hook.load_file(
            filename=tmp_file_path,
            key=s3_key,
            bucket_name=S3_BUCKET,
            replace=True
        )
        print(f"Файл {tmp_file_path} успешно загружен в s3://{S3_BUCKET}/{s3_key}")

        # Удаляем временный файл после загрузки
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            print(f"Временный файл удалён: {tmp_file_path}")

        return f"s3://{S3_BUCKET}/{s3_key}"

    except Exception as e:
        print(f"Ошибка в работе метода upload_to_minio: {e}")


# === Динамический start_date: 5 дней назад от сегодня ===
TODAY = datetime.now().date()
START_DATE = TODAY - timedelta(days=5)
dag_start_date = datetime.combine(START_DATE, datetime.min.time())
# =======================================================

with DAG(
    dag_id="t_invest_load",
    description="Получение данных акций компаний",
    start_date=dag_start_date,
    schedule="*/5 * * * *",
    catchup=False,
    tags=["stocks", "акции", "t-bank"],
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:


    get_stock_price_task = PythonOperator(
        task_id="get_stock_price",
        python_callable=get_stock_price,
        op_kwargs={
            "token": TOKEN
        },
        do_xcom_push=True
    )

    upload_task = PythonOperator(
        task_id="upload_to_minio",
        python_callable=upload_to_minio,
    )

    get_stock_price_task >> upload_task


