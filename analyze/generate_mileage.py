import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def get_dates_from_db():
    """Получение уникальных дат из базы данных"""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT date FROM expenses ORDER BY date")
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dates

def get_vehicles_from_db():
    """Получение списка транспортных средств из базы данных"""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, manufacturer, model FROM vehicles")
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles

def get_category_id(category_name):
    """Получение id категории по имени"""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    category_id = cursor.fetchone()
    conn.close()
    return category_id[0] if category_id else None

def generate_mileage_data():
    """Генерация данных о пробеге"""
    dates = get_dates_from_db()
    vehicles = get_vehicles_from_db()
    
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
    category_id = get_category_id('Пробег')
    
    if not category_id:
        # Если категории нет, создаем её
        conn = sqlite3.connect('expenses.db')
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
                'description': f'Пробег {manufacturer} {model}',
                'vehicle_id': vehicle_id
            })
    
    return mileage_data, vehicle_total_mileage

def import_mileage_to_db(mileage_data, vehicle_total_mileage):
    """Импорт данных о пробеге в базу данных"""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    # Создаем временную таблицу для новых данных
    cursor.execute('''
    CREATE TEMPORARY TABLE temp_mileage (
        date TEXT NOT NULL,
        amount INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        description TEXT,
        vehicle_id INTEGER NOT NULL
    )
    ''')
    
    # Заполняем временную таблицу
    for data in mileage_data:
        cursor.execute('''
        INSERT INTO temp_mileage (date, amount, category_id, description, vehicle_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (data['date'], data['amount'], data['category_id'], 
              data['description'], data['vehicle_id']))
    
    # Удаляем старые записи о пробеге
    cursor.execute("DELETE FROM expenses WHERE category_id = ?", 
                  (mileage_data[0]['category_id'],))
    
    # Копируем новые данные в основную таблицу
    cursor.execute('''
    INSERT INTO expenses (date, amount, category_id, description)
    SELECT date, amount, category_id, description FROM temp_mileage
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

if __name__ == '__main__':
    # Генерируем данные о пробеге
    mileage_data, vehicle_total_mileage = generate_mileage_data()
    
    # Импортируем в базу данных
    import_mileage_to_db(mileage_data, vehicle_total_mileage)
    
    print(f"Успешно сгенерировано и импортировано {len(mileage_data)} записей о пробеге")
    print("\nОбщий пробег по машинам:")
    for vehicle_id, mileage in vehicle_total_mileage.items():
        print(f"Машина {vehicle_id}: {mileage} км") 