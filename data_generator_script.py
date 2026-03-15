# 2. Определение функции для генерации данных
# - определение констант для количества строк и типов данных
# - генерация пользовательских данных (имя, возраст, адрес, дата регистрации и т.д.)
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
    users_count = random.randint(130, 300)

    registration_per_day = []
    for day in range(delta):
        registrations = users_activity_min + random.randint(0, 3)  # Генерируем от 5 до 8 регистраций в день
        registration_per_day.append(registrations)
    
    total_registrations = sum(registration_per_day)
    if total_registrations < users_count:   # Если общее количество регистраций меньше, чем нужно, добавляем дополнительные регистрации
        registrations_to_add = users_count - total_registrations
        for day in range(delta):
            if registrations_to_add <= 0:
                break
            additional_registrations = min(registration_per_day[day] + random.randint(0, 3), users_activity_min + 3) - registration_per_day[day]
            registration_per_day[day] += additional_registrations
            registrations_to_add -= additional_registrations
    elif total_registrations > users_count:  # Если общее количество регистраций больше, чем нужно, уменьшаем регистрации
        registrations_to_remove = total_registrations - users_count
        for day in range(delta):
            if registrations_to_remove <= 0:
                break
            removable_registrations = min(registration_per_day[day] - users_activity_min, registrations_to_remove)
            registration_per_day[day] -= removable_registrations
            registrations_to_remove -= removable_registrations




