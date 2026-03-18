import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

USERS_CSV = 'users.csv'
TOPICS_CSV = 'topics.csv'
MESSAGES_CSV = 'messages.csv'
LOGS_CSV = 'logs.csv'

def load_data_to_db():
    try:
        conn = psycopg2.connect(
            host = 'localhost',
            port = 5432,
            database = 'forum_db',
            user = 'postgres',
            password = 'password'
        )
        cursor = conn.cursor()
        print("Подключение к базе данных успешно установлено.")
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise

    try:
        users_df = pd.read_csv(USERS_CSV)
        topics_df = pd.read_csv(TOPICS_CSV)
        messages_df = pd.read_csv(MESSAGES_CSV)
        logs_df = pd.read_csv(LOGS_CSV)
        print("Данные успешно загружены из CSV файлов.")
    except Exception as e:
        print(f"Ошибка при загрузке данных из CSV файлов: {e}")
        raise




        
   
