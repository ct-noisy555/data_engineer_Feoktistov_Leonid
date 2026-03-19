# Скрипт для агрегации логов форума и сохранения их в CSV файл
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

def new_accounts(cur, start_date, end_date):
    query = """
        SELECT
            DATE_TRUNC('day', registration_date) as day,
            count(*) as new_accounts
        FROM users
        WHERE registration_date >= %s AND registration_date <= %s
        GROUP BY day
        ORDER BY day;
        """
    cur.execute(query, (start_date, end_date))
    return pd.DataFrame(cur.fetchall(), columns=['day', 'new_accounts'])

def messages(cur, start_date, end_date):
    query = """
        SELECT 
            DATE(action_date) as day,
            COUNT(*) as total_messages,
            COUNT(*) FILTER (where user_id is null) as anon_messages
            from logs
            where action_type = 'write_message' and action_date >= %s and action_date <= %s
            group by day
            order by day;
        """
    cur.execute(query, (start_date, end_date))
    message_df = cur.fetchall()

    percentages = []
    for row in message_df:
        day, total_messages, anon_messages = row
        percent = (anon_messages / total_messages * 100) if total_messages > 0 else 0
        percentages.append({
            'day': day,
            'anon_messages_percentage': percent,
            'total_messages': total_messages,
        })
    return pd.DataFrame(percentages, columns=['day', 'anon_messages_percentage', 'total_messages'])

def topic_changes(cur, start_date, end_date):
    query = """
        with daily_topics as (
            select 
                DATE(action_date) as day,
                sum(case when action_type = 'create_topic' and server_response = true then 1 else 0 end) as created,
                sum(case when action_type = 'delete_topic' and server_response = true then 1 else 0 end) as deleted
            from logs
            where action_type in ('create_topic', 'delete_topic') and action_date >= %s and action_date <= %s
            group by date(action_date)
            ),
        cumulative as (
            select 
                day,
                created,
                deleted,
                sum(created-deleted) over (order by day) as total_topics
            from daily_topics
        )
        select 
            day,
            total_topics,
            lag(total_topics) over (order by day) as previous_total,
            case
                when lag(total_topics) over (order by day) > 0
                then round(
                    ((total-topics - lag(total_topics) over (order by day))::float / lag(total_topics) over (order by day) * 100)::numeric, 2
                )
                else 0
            end as percentage_change
        from cumulative
        order by day;
        """
    cur.execute(query, (start_date, end_date))
    return pd.DataFrame(cur.fetchall(), columns=['day', 'total_topics', 'previous_total', 'percentage_change'])



