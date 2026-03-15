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
    users_regs = []
    for day in range(delta):
        users_regs.append(random.randint(5, 10))  # генерация количества регистраций пользователей в день

    





