import sqlite3
import json
from pathlib import Path

def db_to_json(db_path, output_path):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Получаем список всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Создаем словарь для хранения данных всех таблиц
    db_data = {}
    
    # Для каждой таблицы получаем данные
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Получаем имена колонок
        columns = [description[0] for description in cursor.description]
        
        # Получаем все строки
        rows = cursor.fetchall()
        
        # Преобразуем данные в список словарей
        table_data = []
        for row in rows:
            table_data.append(dict(zip(columns, row)))
        
        db_data[table_name] = table_data
    
    # Закрываем соединение с базой данных
    conn.close()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(db_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    db_path = Path(__file__).parent.parent / "data.db"
    output_path = Path(__file__).parent.parent / "data.json"
    

    db_to_json(db_path, output_path)
    print(f"База данных успешно конвертирована в {output_path}") 