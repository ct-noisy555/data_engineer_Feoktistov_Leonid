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

    users_ids = []
    emails = []
    phones = []
    nicknames = []
    registration_dates = []
    topic_count = []
    messages_count = []
    created_at = []
    updated_at = []

    first_visit_logs = []
    registration_logs = []
    current_user_id = 1
    for day in range(delta):    # итерация по дням для генерации данных о пользователях
        users_regs = (random.randint(users_activity_min, 10))  # генерация количества регистраций пользователей в день
        for _ in range(users_regs):  # итерация по количеству регистраций в течение дня
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

            first_visit_time = created_at[-1] - timedelta(minutes=random.randint(1, 60)) #логика для генерации времени первого визита, который происходит за 1-60 минут до регистрации
            first_visit_logs.append({
                'user_id': users_ids[-1],
                'topic_id': None,
                'message_id': None,
                'action_type': 'first_visit',
                'server_response': True,
                'action_date': first_visit_time
            })

            registration_logs.append({
                'user_id': users_ids[-1],
                'topic_id': None,
                'message_id': None,
                'action_type': 'registration',
                'server_response': True,
                'action_date': created_at[-1]
            })

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

                topic_logs.append({
                    'user_id': user_ids[-1],
                    'topic_id': current_topic_id - 1,
                    'message_id': None,
                    'action_type': 'topic_create',
                    'server_response': True,
                    'action_date': creation_time
                })  

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
    #содержание на основе структуры таблицы из .sql файла
    message_ids = []
    topics_ids = []
    users_ids = []
    contents = []
    created_at = []
    updated_at = []

    message_logs = []
    current_message_id = 1

    for day in range(delta): # итерация по дням для генерации данных о сообщениях
        daily_messages_creations_number = random.randint(users_activity_min, 10)
        loged_messages = 0
        anon_messages = 0
        for _ in range(daily_messages_creations_number): # итерация по созданным сообщениям в течение дня
            hour = random.randint(0,23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            creation_time = first_date + timedelta(days=day, hours=hour, minutes=minute, seconds=second)

            is_anon = False

            if anon_messages == loged_messages: #логика для определения анонимного сообщения, чтобы не было перекоса в одну из категорий. Если количество анонимных и логированных сообщений равно - выбор происходит случайно, если же одна из категорий отстает - следующее сообщение будет из этой категории
                is_anon = random.choice([True, False])
            elif anon_messages < loged_messages:
                is_anon = True
            else:
                is_anon = False

            if is_anon:
                users_ids.append(None)
                anon_messages += 1
            else:
                users_ids.append(users_df['user_id'].sample().item()) # выбор пользователя-автора сообщения из ранней генерации пользователей
                loged_messages += 1
                users_df.loc[users_df['user_id'] == users_ids[-1], 'messages_count'] += 1 #увеличение счетчика сообщений у пользователя при создании им сообщения

            message_ids.append(current_message_id)
            topics_ids.append(topics_df['topic_id'].sample().item())
            contents.append(fake.text(max_nb_chars=160))
            created_at.append(creation_time)
            updated_at.append(creation_time)
            current_message_id += 1

            message_logs.append({
                'user_id': users_ids[-1],
                'topic_id': topics_ids[-1],
                'message_id': message_ids[-1],
                'action_type': 'message_create',
                'server_response': True,
                'action_date': creation_time
            })

    messages_df = pd.DataFrame({
        'message_id': message_ids,
        'topic_id': topics_ids,
        'user_id': users_ids,
        'content': contents,
        'created_at': created_at,
        'updated_at': updated_at
    })

    return messages_df

def generate_logs(users_df, topics_df, messages_df):
    logs = []
    logs.extend(topic_logs)
    logs.extend(message_logs)

    for day in range(delta): # итерация по дням для генерации данных о действиях пользователей
        for action in users_activity_types: # итерация по типам действий пользователей в течение дня. 
            daily_type_actions = random.randint(users_activity_min, 10)
            for _ in range (daily_type_actions): # итерация по количеству действий каждого типа в течение дня
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0,59)
                action_time = first_date + timedelta(days=day, hours=hour, minutes=minute, seconds=second)

                if action == 'first_visit':
                    logs.append({
                        'user_id': None,
                        'topic_id': None,
                        'message_id': None,
                        'action_type': 'first_visit',
                        'server_response': True,
                        'action_date': action_time
                    })
                elif action == 'registration':



    