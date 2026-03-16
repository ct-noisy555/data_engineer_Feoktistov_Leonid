# - создание DataFrame из сгенерированных данных
# - возвращение DataFrame с сгенерированными данными
# - генерация тем и аналогично тому, что выше для остальных данных таблиц
# 3. Вызов функции генерации данных и сохранение в файл

import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import numpy as np

fake = Faker('ru_RU')

#константы действий пользователя из первого пункта задания
users_activity_types = ['first_visit', 'registration', 'login', 'logout', 'topic_create', 'topic_visit', 'topic_delete', 'message_create']

#количество дней между первой и последней датой для генерации данных
first_date = datetime(2026, 2, 1)
last_date = datetime(2026, 2, 28)
delta = (last_date - first_date).days + 1

#минимальное количество действий пользователя в день(5), ошибок создания темы(2)
users_activity_min = 5
topic_errors_min = 2

#функция генерации пользователей
def generate_users():
    users_regs = []
    for day in range(delta):
        users_regs.append(random.randint(users_activity_min, 10))  # генерация количества регистраций пользователей в день

    users_ids = []
    emails = []
    phones = []
    nicknames = []
    registration_dates = []
    topic_count = []
    messages_count = []
    created_at = []
    updated_at = []

    current_user_id = 1
    for day in range(delta):    # итерация по дням для генерации данных о пользователях
        for _ in range(users_regs[day]):  # итерация по количеству регистраций в течение дня
            users_ids.append(current_user_id)
            emails.append(fake.email())
            phones.append(fake.phone_number())
            nicknames.append(fake.user_name())
            registration_dates.append(first_date + timedelta(days=day))
            topic_count.append(random.randint(0, 5))    # мб удалю
            messages_count.append(random.randint(0, 5)) # мб удалю
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0,59)
            created_at.append(first_date + timedelta(days=day, hours=hour, minutes=minute, seconds=second))
            updated_at.append(first_date + timedelta(days=day))
            current_user_id += 1

    users_df = pd.DataFrame({
        'user_id': users_ids,
        'email': emails,
        'phone': phones,
        'nickname': nicknames,
        'registration_date': registration_dates,
        'topic_count': topic_count,
        'messages_count': messages_count,
        'created_at': created_at,
        'updated_at': updated_at
    })    
    return users_df

#функция генерации тем
def generate_topics(users_df):
    #содержание на основе структуры таблицы из .sql файла
    topic_ids = []
    user_ids = []
    titles = []
    deleted_at = []
    created_at = []
    updated_at = []

    topic_logs = []
    current_topic_id = 1

    for day in range(delta):  # итерация по дням для генерации данных о темах
        topic_create_errors = 0
        daily_topics_creations_number = random.randint(users_activity_min, 10)
        for _ in range(daily_topics_creations_number): # итерация по количеству созданных тем в течение дня  
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0,59)
            creation_time = first_date + timedelta(days=day, hours=hour, minutes=minute, seconds=second)

            is_error = False

            if topic_create_errors < topic_errors_min:                         #ранее была логика, что создаются первые две ошибки/был риск оказаться без ошибок вовсе
                if random.random() < 0.3:                                      #теперь "случайно" создаются ошибки, а если остается мало тем на день - принудительно.
                    is_error = True 
                    topic_create_errors += 1

            remaining_attempts = daily_topics_creations_number - i + 1
            remaining_errors = topic_errors_min - topic_create_errors

            if remaining_errors > remaining_attempts:
                is_error = True
                topic_create_errors += 1

            if is_error:
                topic_logs.append({
                        'user_id': None,
                        'topic_id': None,
                        'message_id': None,
                        'action_type': 'create_topic',
                        'server_response': False,
                        'action_date': creation_time
                    })               
            else:
                    topic_ids.append(current_topic_id)
                    user_ids.append(users_df['user_id'].sample().item()) # выбор пользователя-создателя темы из ранней генерации пользователей
                    titles.append(fake.sentence(nb_words=6))
                    hour = random.randint(0, 23)
                    minute = random.randint(0, 59)
                    second = random.randint(0,59)
                    created_at.append(creation_time)
                    updated_at.append(creation_time)
                    deleted_at.append(None)
                    current_topic_id += 1

    topics_df = pd.DataFrame({
        'topic_id': topic_ids,
        'user_id': user_ids,
        'title': titles,
        'deleted_at': deleted_at,
        'created_at': created_at,
        'updated_at': updated_at
    })

    return topics_df

#функция генерации сообщений
def generate_messages(users_df, topics_df):