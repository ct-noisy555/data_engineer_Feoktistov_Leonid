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

def date_format_checker(date_string):
    if len(date_string) == 8 and date_string.isdigit():
        for fmt in ['%d%m%Y', '%Y%m%d', '%m%d%Y']:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue

    for sep in ['-', '/', '.', ' ']:
        for fmt in ['%d{sep}%m{sep}%Y', '%Y{sep}%m{sep}%d', '%m{sep}%d{sep}%Y']:   # попробую избавиться от возможной путаницы порядка дат, если успею до сдачи задания. Пока для России норм, первым стоит
            try:
                return datetime.strptime(date_string, fmt.format(sep=sep))
            except ValueError:
                continue
    raise ValueError(f"Не удалось распознать формат даты: {date_string}")
    
def parse_arguments():
    parser = argparse.ArgumentParser(description='Скрипт для агрегации логов форума и сохранения их в CSV файл')
    parser.add_argument('--start_date', required=True, help='Начальная дата')
    parser.add_argument('--end_date', required=True, help='Конечная дата')
    parser.add_argument('--output_file', default='aggregated_logs.csv', help='Имя выходного CSV файла')

    return parser.parse_args()
    
def validate_dates(args):
    try:
        start_date = date_format_checker(args.start_date)
        end_date = date_format_checker(args.end_date)
        if start_date > end_date:
            raise ValueError("Начальная дата не может быть позже конечной даты.")
        return start_date, end_date
    except ValueError as e:
        print(f"Ошибка при обработке дат: {e}")
        raise
    
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



