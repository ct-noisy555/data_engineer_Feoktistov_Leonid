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

    try:
        users_df = pd.read_csv(USERS_CSV)
        topics_df = pd.read_csv(TOPICS_CSV)
        messages_df = pd.read_csv(MESSAGES_CSV)
        logs_df = pd.read_csv(LOGS_CSV)
        print("Данные успешно загружены из CSV файлов.")
    except Exception as e:
        print(f"Ошибка при загрузке данных из CSV файлов: {e}")
        raise
    return cur, users_df, topics_df, messages_df, logs_df, conn

def insert_users_to_db(cur, users_df, conn):
    try:
        data = [tuple(x) for x in users_df.to_numpy()] # преобразуем DataFrame в список кортежей
        execute_values(cur, "INSERT INTO users (id, email, phone, nickname, registration_date, topics_count, messages_count, created_at, updated_at) VALUES %s", data)
        conn.commit()
        print("Данные пользователей успешно вставлены в базу данных.")
    except Exception as e:
        print(f"Ошибка при вставке данных пользователей в базу данных: {e}")
        conn.rollback()
        raise

def insert_topics_to_db(cur, topics_df, conn):
    try:
        topics_df_clean = topics_df.replace({np.nan: None})
        data = [tuple(x) for x in topics_df_clean.to_numpy()] # преобразуем DataFrame в список кортежей
        execute_values(cur, "INSERT INTO topic(id, user_id, title, deleted_at, created_at, updated_at) VALUES %s", data)
        conn.commit()
        print("Данные тем успешно вставлены в базу данных.")
    except Exception as e:
        print(f"Ошибка при вставке данных тем в базу данных: {e}")
        conn.rollback()
        raise

def insert_messages_to_db(cur, messages_df, conn):
    try:
        messages_df_clean = messages_df.replace({np.nan: None})
        data = [tuple(x) for x in messages_df_clean.to_numpy()] # преобразуем DataFrame в список кортежей
        execute_values(cur, "INSERT INTO messages (id, topic_id, user_id, content, created_at, updated_at) VALUES %s", data)
        conn.commit()
        print("Данные сообщений успешно вставлены в базу данных.")
    except Exception as e:
        print(f"Ошибка при вставке данных сообщений в базу данных: {e}")
        conn.rollback()
        raise

def insert_logs_to_db(cur, logs_df, conn):
    try:
        logs_df_clean = logs_df.replace({np.nan: None})
        data = [tuple(x) for x in logs_df_clean.to_numpy()] # преобразуем DataFrame в список кортежей
        execute_values(cur, "INSERT INTO logs (id, user_id, topic_id, message_id, action_type, server_response, action_date) VALUES %s", data)
        conn.commit()
        print("Данные логов успешно вставлены в базу данных.")
    except Exception as e:
        print(f"Ошибка при вставке данных логов в базу данных: {e}")
        conn.rollback()
        raise

if __name__ == "__main__":
    try:
        print("Загрузка данных из CSV файлов и вставка в базу данных...")
        cur, users_df, topics_df, messages_df, logs_df, conn = load_data_to_db()
    except Exception as e:
        print(f"Ошибка при загрузке данных из CSV файлов: {e}")
        raise
    try:
        print("\tНачинаю вставку данных пользователей в базу данных...")
        insert_users_to_db(cur, users_df, conn)
    except Exception as e:
        print(f"Ошибка при вставке данных пользователей: {e}")
        conn.rollback()
        raise
    try:
        print("\tВставляю данные тем в базу данных...")
        insert_topics_to_db(cur, topics_df, conn)
    except Exception as e:
        print(f"Ошибка при вставке данных тем: {e}")
        conn.rollback()
        raise
    try:
        print("\tВставляю данные сообщений в базу данных...")
        insert_messages_to_db(cur, messages_df, conn)
    except Exception as e:
        print(f"Ошибка при вставке данных сообщений: {e}")
        conn.rollback()
        raise
    try:
        print("\tВставляю данные логов в базу данных...")
        insert_logs_to_db(cur, logs_df, conn)
    except Exception as e:
        print(f"Ошибка при вставке данных логов: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
        print("Подключение к базе данных закрыто.")




        
   
