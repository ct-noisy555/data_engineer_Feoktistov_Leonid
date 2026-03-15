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
users_activity_types = ['first_visit', 'registration', 'logIn', 'logOut', 'topic_create', 'topic_visit', 'topic_delete', 'message_create']

#количество дней между первой и последней датой для генерации данных
first_date = datetime(2026, 2, 1)
last_date = datetime(2026, 2, 28)
delta = (last_date - first_date).days + 1

#минимальное количество действий пользователя в день(5), действий создания темы(2)
users_activity_min = 5
topic_errors_min = 2

#функция генерации пользователей
def generate_users():
    users_regs = []
    for day in range(delta):
        users_regs.append(random.randint(5, 10))  # генерация количества регистраций пользователей в день

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
            created_at.append(first_date + timedelta(days=day))
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


    





