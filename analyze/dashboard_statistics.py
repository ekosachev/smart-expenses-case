import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List

class SQLiteDataSource:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_data(self) -> List[Dict[str, Any]]:
        """Получение данных из SQLite базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Обновленный SQL-запрос с учетом структуры таблицы vehicles
        query = """
        SELECT 
            e.date,
            e.amount,
            c.name as category,
            e.description,
            v.manufacturer || ' ' || v.model as vehicle_name,
            e.ID_car
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        JOIN vehicles v ON e.ID_car = v.id
        ORDER BY e.date
        """
        
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return data

def create_data_source(source_type: str, **kwargs) -> SQLiteDataSource:
    """Создание источника данных"""
    if source_type == 'sqlite':
        return SQLiteDataSource(kwargs.get('db_path', 'expenses.db'))
    else:
        raise ValueError(f"Неподдерживаемый тип источника данных: {source_type}")

def get_dashboard_statistics(source_type: str = 'sqlite', **kwargs) -> Dict[str, Any]:
    """Получение статистики для дашборда"""
    data_source = create_data_source(source_type, **kwargs)
    data = data_source.get_data()
    
    # Инициализация статистики
    statistics = {
        'category_statistics': {},
        'vehicle_statistics': {},
        'total_statistics': {
            'total_amount': 0,
            'average_amount': 0,
            'max_amount': 0,
            'min_amount': float('inf'),
            'count': 0
        }
    }
    
    # Обработка данных
    for record in data:
        category = record['category']
        amount = float(record['amount'])
        vehicle_name = record['vehicle_name']
        
        # Статистика по категориям
        if category not in statistics['category_statistics']:
            statistics['category_statistics'][category] = {
                'total': 0,
                'average': 0,
                'max': 0,
                'min': float('inf'),
                'count': 0
            }
        
        cat_stats = statistics['category_statistics'][category]
        cat_stats['total'] += amount
        cat_stats['count'] += 1
        cat_stats['max'] = max(cat_stats['max'], amount)
        cat_stats['min'] = min(cat_stats['min'], amount)
        
        # Статистика по транспортным средствам
        if vehicle_name not in statistics['vehicle_statistics']:
            statistics['vehicle_statistics'][vehicle_name] = {
                'total': 0,
                'average': 0,
                'max': 0,
                'min': float('inf'),
                'count': 0
            }
        
        veh_stats = statistics['vehicle_statistics'][vehicle_name]
        veh_stats['total'] += amount
        veh_stats['count'] += 1
        veh_stats['max'] = max(veh_stats['max'], amount)
        veh_stats['min'] = min(veh_stats['min'], amount)
        
        # Общая статистика
        total_stats = statistics['total_statistics']
        total_stats['total_amount'] += amount
        total_stats['count'] += 1
        total_stats['max_amount'] = max(total_stats['max_amount'], amount)
        total_stats['min_amount'] = min(total_stats['min_amount'], amount)
    
    # Вычисление средних значений
    for category in statistics['category_statistics']:
        stats = statistics['category_statistics'][category]
        stats['average'] = stats['total'] / stats['count'] if stats['count'] > 0 else 0
    
    for vehicle in statistics['vehicle_statistics']:
        stats = statistics['vehicle_statistics'][vehicle]
        stats['average'] = stats['total'] / stats['count'] if stats['count'] > 0 else 0
    
    total_stats = statistics['total_statistics']
    total_stats['average_amount'] = total_stats['total_amount'] / total_stats['count'] if total_stats['count'] > 0 else 0
    
    return statistics

def save_statistics(statistics: Dict[str, Any], output_file: str = 'dashboard_statistics.json'):
    """Сохранение статистики в JSON файл"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(statistics, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # Пример использования
    statistics = get_dashboard_statistics('sqlite', db_path='expenses.db')
    save_statistics(statistics)
    print(f"Статистика сохранена в файл dashboard_statistics.json") 