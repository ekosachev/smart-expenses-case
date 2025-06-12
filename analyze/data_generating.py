import pandas as pd
import sqlite3
import json
import os
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import numpy as np
import random

# --- Глобальные константы из generate_vehicles.py ---
MANUFACTURERS = {
    'КАМАЗ': {
        'models': ['6520', '5320', '43118', '5490', '65115'],
        'type': 'грузовой',
        'passenger_capacity': 2,
        'fuel_consumption': [25, 35],  # л/100км
        'price_range': [2500000, 4500000]  # руб
    },
    'ГАЗ': {
        'models': ['ГАЗель NEXT', 'Соболь', 'Валдай', 'ГАЗон NEXT'],
        'type': 'грузовой',
        'passenger_capacity': 2,
        'fuel_consumption': [12, 18],
        'price_range': [1500000, 2500000]
    },
    'УАЗ': {
        'models': ['Патриот', 'Хантер', 'Профи', 'Буханка'],
        'type': 'пассажирский',
        'passenger_capacity': 7,
        'fuel_consumption': [12, 15],
        'price_range': [1200000, 2000000]
    },
    'LADA': {
        'models': ['Гранта', 'Веста', 'Ларгус', 'Нива'],
        'type': 'пассажирский',
        'passenger_capacity': 5,
        'fuel_consumption': [7, 10],
        'price_range': [800000, 1500000]
    },
    'Hyundai': {
        'models': ['Solaris', 'Creta', 'Tucson', 'Santa Fe'],
        'type': 'пассажирский',
        'passenger_capacity': 5,
        'fuel_consumption': [6, 9],
        'price_range': [1200000, 2500000]
    }
}

# --- Функции из import_to_db.py ---
def import_csv_to_db_func(csv_path: str, db_path: str = os.path.join(os.path.pardir, 'data.db')):
    df = pd.read_csv(csv_path)
    _import_df_to_db_func(df, db_path)

def import_json_to_db_func(json_path: str, db_path: str = os.path.join(os.path.pardir, 'data.db')):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    _import_df_to_db_func(df, db_path)

def _import_df_to_db_func(df: pd.DataFrame, db_path: str):
    required = {'Дата', 'Сумма', 'Категория'}
    if not required.issubset(df.columns):
        raise ValueError(f'В файле должны быть колонки: {required}')
    
    categories = df['Категория'].dropna().unique()
    cat_df = pd.DataFrame({'name': categories})
    cat_df['id'] = range(1, len(cat_df) + 1)
    
    cat_map = dict(zip(cat_df['name'], cat_df['id']))
    df['category_id'] = df['Категория'].map(cat_map)
    
    # Извлекаем числовой ID из столбца 'Автомобиль' для ID_car и обеспечиваем целочисленный тип
    if 'Автомобиль' in df.columns:
        df['ID_car'] = df['Автомобиль'].apply(lambda x: int(x.split('_')[1]) if pd.notna(x) and isinstance(x, str) and '_' in x else 0)
    else:
        df['ID_car'] = 0 # Значение по умолчанию, если столбец 'Автомобиль' отсутствует

    expenses_df = pd.DataFrame({
        'date': pd.to_datetime(df['Дата']).dt.strftime('%Y-%m-%d'),
        'amount': df['Сумма'],
        'category_id': df['category_id'],
        'ID_car': df['ID_car']
    })
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Создаем таблицы, если они не существуют
    cur.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category_id INTEGER,
        ID_car INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')
    
    cat_df[['id', 'name']].to_sql('categories', conn, if_exists='append', index=False)
    expenses_df.to_sql('expenses', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print(f'Данные успешно импортированы в {db_path}')

# --- Функции из sum_mileage_by_vehicle.py ---
def update_total_mileage_func(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем id категории "Пробег"
    cursor.execute("SELECT id FROM categories WHERE name = 'Пробег'")
    row = cursor.fetchone()
    if not row:
        print('Категория "Пробег" не найдена!')
        conn.close()
        return
    mileage_cat_id = row[0]
    
    # Считаем сумму пробега по каждой машине
    cursor.execute('''
        SELECT ID_car, SUM(amount) FROM expenses
        WHERE category_id = ?
        GROUP BY ID_car
    ''', (mileage_cat_id,))
    results = cursor.fetchall()
    
    # Обновляем значения в таблице vehicles
    for ID_car, total_mileage in results:
        cursor.execute('''
            UPDATE vehicles SET total_mileage = ? WHERE id = ?
        ''', (total_mileage, ID_car))
    conn.commit()
    conn.close()
    print('Общий пробег по каждой машине успешно обновлён!')

def _check_expenses_table_schema(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(expenses)")
    schema = cursor.fetchall()
    print("\nСхема таблицы expenses:")
    for col in schema:
        print(col)
    conn.close()

def generate_monthly_budget_table_func(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    conn = sqlite3.connect(db_path)
    
    # Получаем расходы по категориям 1-8 и ID_car
    query = """
    SELECT
        strftime('%Y', date) AS year,
        strftime('%m', date) AS month,
        ID_car,
        amount
    FROM expenses
    WHERE category_id BETWEEN 1 AND 8;
    """
    
    all_relevant_expenses_df = pd.read_sql_query(query, conn)
    
    if all_relevant_expenses_df.empty:
        print("Нет данных для генерации ежемесячного бюджета.")
        conn.close()
        return

    # Группируем для фактических расходов
    actual_expenses_df = all_relevant_expenses_df.groupby(['year', 'month', 'ID_car'])['amount'].sum().reset_index()
    actual_expenses_df.rename(columns={'amount': 'actual_expenses_rub'}, inplace=True)

    # Рассчитываем средний расход на каждую машину по категориям 1-8 за весь период для планируемого бюджета
    # Это будет нашей базовой "планируемой" суммой для каждой машины в месяц
    planned_budget_base_df = all_relevant_expenses_df.groupby('ID_car')['amount'].mean().reset_index()
    planned_budget_base_df.rename(columns={'amount': 'avg_monthly_amount_per_car'}, inplace=True)

    # Объединяем фактические расходы с базовыми значениями планируемого бюджета
    monthly_budget_df = pd.merge(actual_expenses_df, planned_budget_base_df, on='ID_car', how='left')
    
    # Заполняем NaN в planned_budget_rub (для машин, по которым не было данных для расчета средней)
    # используя общий средний расход по всем машинам
    overall_avg_amount = all_relevant_expenses_df['amount'].mean()
    
    monthly_budget_df['planned_budget_rub'] = monthly_budget_df['avg_monthly_amount_per_car'].fillna(overall_avg_amount)
    
    # Корректируем планируемый бюджет, чтобы он был чуть выше фактического, но не всегда
    monthly_budget_df['planned_budget_rub'] = monthly_budget_df.apply(
        lambda row: row['actual_expenses_rub'] * (1 + np.random.uniform(0.02, 0.10))
                    if row['actual_expenses_rub'] > row['planned_budget_rub'] and np.random.random() < 0.7
                    else row['planned_budget_rub'],
        axis=1
    )

    # Добавляем столбец процента фактических трат от планируемых
    monthly_budget_df['percentage_of_planned'] = (monthly_budget_df['actual_expenses_rub'] / monthly_budget_df['planned_budget_rub']) * 100
    
    # Выбираем и переименовываем столбцы для итоговой таблицы
    final_budget_df = monthly_budget_df[['month', 'year', 'ID_car', 'planned_budget_rub', 'actual_expenses_rub', 'percentage_of_planned']]
    final_budget_df.rename(columns={'month': 'Месяц', 'year': 'Год', 'ID_car': 'ID_машины', 'planned_budget_rub': 'Планируемый_бюджет_руб', 'actual_expenses_rub': 'Фактические_расходы_руб', 'percentage_of_planned': 'Процент_от_плана'}, inplace=True)
    
    # Сохраняем в новую таблицу monthly_budget
    final_budget_df.to_sql('monthly_budget', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    print('Ежемесячный бюджет успешно рассчитан и сохранён в таблице monthly_budget.')

# --- Функции из generate_expenses.py ---
def generate_expenses_data_func(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    np.random.seed(42)
    random.seed(42)

    start_date = "2023-01-01"
    end_date = "2025-06-20"
    num_vehicles = 20

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    vehicle_ids = [f"Car_{i}" for i in range(1, num_vehicles + 1)]
    fuel_prices = np.random.normal(55, 5, len(date_range))

    categories = [
        "Топливо",
        "Ремонт",
        "Налоги",
        "Штрафы",
        "Аренда",
        "Амортизация",
        "Админ_расходы",
        "Логистика"
    ]

    # Месяцы с выбросами
    outlier_months = sorted(random.sample(range(1, 13), 3))
    outlier_categories = {month: random.choice(categories) for month in outlier_months}
    print(f"\nМесяцы с выбросами и их категории:")
    for month, category in outlier_categories.items():
        print(f"Месяц {month}: {category}")

    # Создаем DataFrame для категорий
    cat_df = pd.DataFrame({'name': categories})
    cat_df['id'] = range(1, len(cat_df) + 1)
    cat_map = dict(zip(cat_df['name'], cat_df['id']))

    # Подготавливаем данные для expenses
    expenses_data = []
    id_counter = 1

    for date in date_range:
        num_records_today = np.random.randint(1, 5)
        
        for _ in range(num_records_today):
            vehicle = np.random.choice(vehicle_ids)
            category = np.random.choice(categories)
            days_since_start = (date - pd.to_datetime(start_date)).days
            
            # Проверяем, является ли текущий месяц месяцем с выбросом и текущая категория - категорией выброса
            is_outlier = date.month in outlier_months and category == outlier_categories[date.month]
            
            if category == "Топливо":
                mileage = np.random.normal(200 + 0.15*days_since_start, 50)
                amount = round((mileage/100*12) * fuel_prices[days_since_start])
                if is_outlier:
                    amount *= np.random.uniform(8.0, 12.0) 
            elif category == "Ремонт":
                base_repair = np.random.normal(200 + 0.15*days_since_start, 50) * 0.15
                if date.month in [12, 1, 2]:
                    base_repair *= 1.5
                amount = round(np.random.exponential(base_repair)) if np.random.rand() < 0.15 else 0
                if is_outlier and amount > 0:
                    amount *= np.random.uniform(10.0, 15.0)
            elif category == "Налоги":
                amount = round(1500000 * 0.015 / 365)
                if is_outlier:
                    amount *= np.random.uniform(7.0, 10.0)
            elif category == "Штрафы":
                amount = round(np.random.uniform(500, 5000)) if np.random.rand() < 0.05 else 0
                if is_outlier and amount > 0:
                    amount *= np.random.uniform(8.0, 12.0)
            elif category == "Аренда":
                amount = round(np.random.normal(3000, 500) * (1.07)**((date.year - 2023) + (date.month-1)/12))
                if is_outlier:
                    amount *= np.random.uniform(6.0, 9.0)
            elif category == "Амортизация":
                amount = round(1500000 / (5*365))
                if is_outlier:
                    amount *= np.random.uniform(7.0, 10.0) 
            elif category == "Админ_расходы":
                amount = round(np.random.normal(800, 200))
                if is_outlier:
                    amount *= np.random.uniform(8.0, 12.0) 
            elif category == "Логистика":
                amount = round(np.random.normal(2000, 500))
                if is_outlier:
                    amount *= np.random.uniform(9.0, 13.0) 
            
            if amount > 0:
                vehicle_id = int(vehicle.split('_')[1])
                expenses_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'amount': round(amount),
                    'category_id': cat_map[category],
                    'ID_car': vehicle_id
                })
                id_counter += 1

    # Создаем DataFrame для expenses
    expenses_df = pd.DataFrame(expenses_data)
    
    # Сохраняем данные в базу
    conn = sqlite3.connect(db_path)
    
    # Создаем таблицы, если они не существуют
    cur = conn.cursor()
    # Удаляем таблицы, если они существуют, чтобы гарантировать актуальную схему
    cur.execute('DROP TABLE IF EXISTS expenses')
    cur.execute('DROP TABLE IF EXISTS categories')

    cur.execute('''CREATE TABLE categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )''')
    cur.execute('''CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category_id INTEGER,
        ID_car INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')
    
    # Сохраняем категории
    cat_df[['id', 'name']].to_sql('categories', conn, if_exists='append', index=False)
    
    # Сохраняем расходы
    expenses_df.to_sql('expenses', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print(f"Сгенерировано и сохранено в базу данных {len(expenses_data)} записей")

# --- Функции из generate_mileage.py ---
def get_dates_from_db_mileage(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Получение уникальных дат из базы данных"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT date FROM expenses ORDER BY date")
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dates

def get_vehicles_from_db_mileage(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Получение списка транспортных средств из базы данных"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, manufacturer, model FROM vehicles")
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles

def get_category_id_mileage(category_name: str, db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Получение id категории по имени"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    category_id = cursor.fetchone()
    conn.close()
    return category_id[0] if category_id else None

def generate_mileage_data_func(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Генерация данных о пробеге"""
    dates = get_dates_from_db_mileage(db_path)
    vehicles = get_vehicles_from_db_mileage(db_path)
    
    # Базовые параметры пробега для разных типов транспорта
    mileage_params = {
        'грузовой': {
            'КАМАЗ': {'mean': 300, 'std': 50, 'min': 100, 'max': 500},
            'ГАЗ': {'mean': 250, 'std': 40, 'min': 80, 'max': 400},
            'default': {'mean': 200, 'std': 30, 'min': 50, 'max': 350}
        },
        'пассажирский': {
            'УАЗ': {'mean': 150, 'std': 30, 'min': 40, 'max': 250},
            'LADA': {'mean': 100, 'std': 20, 'min': 30, 'max': 200},
            'Hyundai': {'mean': 120, 'std': 25, 'min': 35, 'max': 220},
            'default': {'mean': 80, 'std': 15, 'min': 20, 'max': 150}
        }
    }
    
    # Генерация данных
    mileage_data = []
    vehicle_total_mileage = {}  # Словарь для хранения общего пробега каждой машины
    category_id = get_category_id_mileage('Пробег', db_path)
    
    if not category_id:
        # Если категории нет, создаем её
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES ('Пробег')")
        category_id = cursor.lastrowid
        conn.commit()
        conn.close()
    
    for vehicle_id, vehicle_type, manufacturer, model in vehicles:
        # Получаем параметры пробега для конкретного транспорта
        params = mileage_params[vehicle_type].get(manufacturer, 
                mileage_params[vehicle_type]['default'])
        
        vehicle_total_mileage[vehicle_id] = 0  # Инициализируем общий пробег
        
        for date in dates:
            # 5% шанс нулевого пробега
            if random.random() < 0.05:
                mileage = 0
            else:
                # Генерация пробега с учетом типа транспорта
                mileage = int(np.random.normal(params['mean'], params['std']))
                mileage = max(params['min'], min(params['max'], mileage))
            
            vehicle_total_mileage[vehicle_id] += mileage  # Увеличиваем общий пробег
            
            mileage_data.append({
                'date': date,
                'amount': mileage,
                'category_id': category_id,
                'vehicle_id': vehicle_id
            })
    
    return mileage_data, vehicle_total_mileage

def import_mileage_to_db_func(mileage_data: List[Dict[str, Any]], vehicle_total_mileage: Dict[int, float], db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Импорт данных о пробеге в базу данных"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем временную таблицу для новых данных
    cursor.execute('''
    CREATE TEMPORARY TABLE temp_mileage (
        date TEXT NOT NULL,
        amount INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL
    )
    ''')
    
    # Заполняем временную таблицу
    for data in mileage_data:
        cursor.execute('''
        INSERT INTO temp_mileage (date, amount, category_id, vehicle_id)
        VALUES (?, ?, ?, ?)
        ''', (data['date'], data['amount'], data['category_id'], data['vehicle_id']))
    
    # Удаляем старые записи о пробеге
    cursor.execute("DELETE FROM expenses WHERE category_id = ?", 
                  (mileage_data[0]['category_id'],))
    
    # Копируем новые данные в основную таблицу
    cursor.execute('''
    INSERT INTO expenses (date, amount, category_id, ID_car)
    SELECT date, amount, category_id, vehicle_id FROM temp_mileage
    ''')
    
    # Обновляем общий пробег в таблице vehicles
    for vehicle_id, total_mileage in vehicle_total_mileage.items():
        cursor.execute('''
        UPDATE vehicles 
        SET total_mileage = ? 
        WHERE id = ?
        ''', (total_mileage, vehicle_id))
        print(f"Обновляем пробег для машины {vehicle_id}: {total_mileage} км")
    
    # Удаляем временную таблицу
    cursor.execute("DROP TABLE temp_mileage")
    
    conn.commit()
    conn.close()

# --- Функции из generate_vehicles.py ---
def generate_plate_number_func():
    """Генерация случайного гос. номера"""
    letters = 'АВЕКМНОРСТУХ'
    return f"{random.choice(letters)}{random.choice(letters)}{random.randint(100, 999)}{random.choice(letters)}{random.choice(letters)}"

def get_vehicle_data_func(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Получение данных о пробеге и аренде из базы данных по category_id"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем id категорий
    cursor.execute("SELECT id FROM categories WHERE name = 'Пробег'")
    row = cursor.fetchone()
    mileage_cat_id = row[0] if row else None
    cursor.execute("SELECT id FROM categories WHERE name = 'Аренда'")
    row = cursor.fetchone()
    rent_cat_id = row[0] if row else None
    
    # Получаем общий пробег
    if mileage_cat_id:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE category_id = ?", (mileage_cat_id,))
        total_mileage = cursor.fetchone()[0] or 0
    else:
        total_mileage = 0
    
    # Получаем стоимость аренды
    if rent_cat_id:
        cursor.execute("SELECT AVG(amount) FROM expenses WHERE category_id = ?", (rent_cat_id,))
        avg_rent = cursor.fetchone()[0] or 0
    else:
        avg_rent = 0
    
    conn.close()
    return total_mileage, avg_rent

def generate_vehicles_func(num_vehicles=20, db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Генерация данных о транспортных средствах"""
    total_mileage, avg_rent = get_vehicle_data_func(db_path)
    vehicles = []
    
    # Распределяем пробег между машинами
    mileage_per_vehicle = total_mileage / num_vehicles
    
    for i in range(num_vehicles):
        manufacturer = random.choice(list(MANUFACTURERS.keys()))
        manufacturer_data = MANUFACTURERS[manufacturer]
        
        vehicle = {
            'id': i + 1,
            'plate_number': generate_plate_number_func(),
            'manufacturer': manufacturer,
            'model': random.choice(manufacturer_data['models']),\
            'year': random.randint(2015, 2024),\
            'type': manufacturer_data['type'],
            'cargo_capacity': random.randint(500, 20000) if manufacturer_data['type'] == 'грузовой' else 0,\
            'passenger_capacity': manufacturer_data['passenger_capacity'],
            'fuel_consumption': random.uniform(*manufacturer_data['fuel_consumption']),\
            'mileage': int(mileage_per_vehicle * random.uniform(0.8, 1.2)),  # ±20% от среднего
            'price': random.randint(*manufacturer_data['price_range']),\
            'rent_price': int(avg_rent * random.uniform(0.8, 1.2))  # ±20% от среднего
        }
        vehicles.append(vehicle)
    
    return vehicles

def create_vehicles_table_func(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Создание таблицы для транспортных средств"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY,
        plate_number TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        type TEXT NOT NULL,
        cargo_capacity INTEGER,\
        passenger_capacity INTEGER NOT NULL,\
        fuel_consumption REAL NOT NULL,\
        mileage INTEGER NOT NULL,\
        price INTEGER NOT NULL,\
        rent_price INTEGER NOT NULL,
        total_mileage INTEGER DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()

def import_vehicles_to_db_func(vehicles: List[Dict[str, Any]], db_path: str = os.path.join(os.path.pardir, 'data.db')):
    """Импорт данных о транспортных средствах в базу данных"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for vehicle in vehicles:
        cursor.execute('''
        INSERT INTO vehicles (
            id, plate_number, manufacturer, model, year, type,
            cargo_capacity, passenger_capacity, fuel_consumption,
            mileage, price, rent_price, total_mileage
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vehicle['id'], vehicle['plate_number'], vehicle['manufacturer'],
            vehicle['model'], vehicle['year'], vehicle['type'],
            vehicle['cargo_capacity'], vehicle['passenger_capacity'],
            vehicle['fuel_consumption'], vehicle['mileage'],
            vehicle['price'], vehicle['rent_price'], 0 # Initial total_mileage
        ))\
    
    conn.commit()
    conn.close()

# --- Основной блок выполнения при запуске data_generating.py ---
if __name__ == '__main__':
    db_file_name = 'data.db'
    db_file_path = os.path.join(os.path.pardir, db_file_name)

    print("\n--- Запуск всех операций управления данными ---")

    # 1. Удаляем существующий файл базы данных, чтобы обеспечить чистоту перед созданием таблиц
    if os.path.exists(db_file_path):
        os.remove(db_file_path)
        print(f"Удален существующий файл базы данных: {db_file_path}")

    # 2. Создаем таблицы (включая categories, expenses и vehicles)
    # import_csv_to_db_func создает categories и expenses, а также импортирует данные
    # Сначала создаем vehicles, так как import_csv_to_db_func будет создавать categories и expenses
    # и затем мы хотим, чтобы vehicles также были созданы.
    create_vehicles_table_func(db_path=db_file_path)

    # 3. Сгенерировать данные о расходах и сохранить в базу данных
    print("\nШаг 1: Генерация данных о расходах...")
    generate_expenses_data_func(db_path=db_file_path)

    # 4. Сгенерировать и импортировать данные о ТС (generate_vehicles.py)
    print("\nШаг 2: Генерация и импорт данных о транспортных средствах...")
    vehicles_data = generate_vehicles_func(db_path=db_file_path)
    import_vehicles_to_db_func(vehicles_data, db_path=db_file_path)
    print(f"Успешно сгенерировано и импортировано {len(vehicles_data)} транспортных средств")

    # 5. Сгенерировать и импортировать данные о пробеге (generate_mileage.py)
    print("\nШаг 3: Генерация и импорт данных о пробеге...")
    mileage_data, vehicle_total_mileage = generate_mileage_data_func(db_path=db_file_path)
    import_mileage_to_db_func(mileage_data, vehicle_total_mileage, db_path=db_file_path)
    print(f"Успешно сгенерировано и импортировано {len(mileage_data)} записей о пробеге")
    print("Общий пробег по машинам:")
    for vehicle_id, mileage in vehicle_total_mileage.items():
        print(f"Машина {vehicle_id}: {mileage} км")

    # 6. Обновить общий пробег в таблице vehicles на основе expenses (sum_mileage_by_vehicle.py)
    print("\nШаг 4: Обновление общего пробега в таблице транспорта...")
    update_total_mileage_func(db_path=db_file_path)

    # 7. Генерация таблицы ежемесячного бюджета
    print("\nШаг 5: Генерация таблицы ежемесячного бюджета...")
    generate_monthly_budget_table_func(db_path=db_file_path)

    print("\n--- Все операции по управлению данными завершены ---")