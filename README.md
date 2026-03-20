# data_engineer_Feoktistov_Leonid
Проект поднятия базы данных и агрегации с данными в ней.
Проект генерирует тестовые данные за месяц, загружает их в PostgreSQL и формирует агрегированный датасет.

## Структура проекта

```
data_engineer_Feoktistov_Leonid/
├── DB_schema_DrawSQL.jpg      # диаграмма схемы базы данных
├── docker-compose.yml         # запуск PostgreSQL в Docker
├── init.sql                   # создание таблиц в БД
│
├── data_generator_script.py   # генерация тестовых данных
├── load_dataset.py            # загрузка CSV файлов в БД
├── data_aggregation_script.py # агрегация данных
│
├── users.csv
├── topics.csv
├── messages.csv
├── logs.csv                   # сгенерированные логи
│
├── aggregated_logs.csv        # результат агрегации
│
└── requirements.txt           # библиотеки для работы

```

## Требования

- **Docker Desktop**
- **Python 3.8+**
- **PostgreSQL 15** (запускается в Docker)

## Установка зависимостей

``` bash
pip install -r requirements.txt
```

## Запуск базы данных
Запуск PostgreSQL в Docker:
``` bash
docker-compose up -d
```

## Инициализация базы
После запуска контейнера создаются таблицы из файла
``` bash
init.sql
```

## Загрузка данных
``` bash
python load_dataset.py
```
Скрипт загружает данные из CSV файлов в базу.

## Агрегация данных
Скрипт:
``` bash
    python data_aggregation_script.py
```
Формирует итоговый CSV:
``` bash
    aggregated_logs.csv
```
## Команда для проверки:

```bash
docker-compose up -d
pip install -r requirements.txt
python data_generator_script.py
python load_dataset.py
python data_aggregation_script.py
```

