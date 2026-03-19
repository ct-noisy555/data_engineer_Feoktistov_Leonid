# Скрипт для агрегации логов форума и сохранения их в CSV файл
# парс даты в любом формате....
# подключение к БД
# проверка валидации данных
# агрегация данных по заданию
# сохранение в CSV файл

import pandas as pd
import psycopg2
import argparse
from datetime import datetime

def parse_arguments():
    

def connect_to_db():
    try:
        conn = psycopg2.connect(
                host = 'localhost',
                port = 5433,
                database = 'forum_logs',
                user = 'postgres',
                password = 'postgres'
            )
            cur = conn.cursor()
            print("Подключение к базе данных успешно установлено.")
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise
    return conn, cur



