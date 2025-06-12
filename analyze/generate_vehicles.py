import random
import sqlite3
from datetime import datetime
import pandas as pd

# Список производителей и моделей
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

def generate_plate_number():
    """Генерация случайного гос. номера"""
    letters = 'АВЕКМНОРСТУХ'
    return f"{random.choice(letters)}{random.choice(letters)}{random.randint(100, 999)}{random.choice(letters)}{random.choice(letters)}"

def get_vehicle_data():
    """Получение данных о пробеге и аренде из базы данных по category_id"""
    conn = sqlite3.connect('expenses.db')
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

def generate_vehicles(num_vehicles=20):
    """Генерация данных о транспортных средствах"""
    total_mileage, avg_rent = get_vehicle_data()
    vehicles = []
    
    # Распределяем пробег между машинами
    mileage_per_vehicle = total_mileage / num_vehicles
    
    for i in range(num_vehicles):
        manufacturer = random.choice(list(MANUFACTURERS.keys()))
        manufacturer_data = MANUFACTURERS[manufacturer]
        
        vehicle = {
            'id': i + 1,
            'plate_number': generate_plate_number(),
            'manufacturer': manufacturer,
            'model': random.choice(manufacturer_data['models']),
            'year': random.randint(2015, 2024),
            'type': manufacturer_data['type'],
            'cargo_capacity': random.randint(500, 20000) if manufacturer_data['type'] == 'грузовой' else 0,
            'passenger_capacity': manufacturer_data['passenger_capacity'],
            'fuel_consumption': random.uniform(*manufacturer_data['fuel_consumption']),
            'mileage': int(mileage_per_vehicle * random.uniform(0.8, 1.2)),  # ±20% от среднего
            'price': random.randint(*manufacturer_data['price_range']),
            'rent_price': int(avg_rent * random.uniform(0.8, 1.2))  # ±20% от среднего
        }
        vehicles.append(vehicle)
    
    return vehicles

def create_vehicles_table():
    """Создание таблицы для транспортных средств"""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY,
        plate_number TEXT NOT NULL,
        manufacturer TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        type TEXT NOT NULL,
        cargo_capacity INTEGER,
        passenger_capacity INTEGER NOT NULL,
        fuel_consumption REAL NOT NULL,
        mileage INTEGER NOT NULL,
        price INTEGER NOT NULL,
        rent_price INTEGER NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def import_vehicles_to_db(vehicles):
    """Импорт данных о транспортных средствах в базу данных"""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    for vehicle in vehicles:
        cursor.execute('''
        INSERT INTO vehicles (
            id, plate_number, manufacturer, model, year, type,
            cargo_capacity, passenger_capacity, fuel_consumption,
            mileage, price, rent_price
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vehicle['id'], vehicle['plate_number'], vehicle['manufacturer'],
            vehicle['model'], vehicle['year'], vehicle['type'],
            vehicle['cargo_capacity'], vehicle['passenger_capacity'],
            vehicle['fuel_consumption'], vehicle['mileage'],
            vehicle['price'], vehicle['rent_price']
        ))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Создаем таблицу
    create_vehicles_table()
    
    # Генерируем данные
    vehicles = generate_vehicles()
    
    # Импортируем в базу данных
    import_vehicles_to_db(vehicles)
    
    print(f"Успешно сгенерировано и импортировано {len(vehicles)} транспортных средств") 