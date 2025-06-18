import sqlite3
import pandas as pd
import csv
from datetime import datetime

def export_expenses_with_categories():
    """Экспорт таблицы expenses с нужными столбцами: license_plate, expense_date, description"""
    conn = sqlite3.connect('data.db')
    
    # SQL запрос для объединения expenses с categories и vehicles
    query = """
    SELECT 
        v.plate_number AS license_plate,
        e.date AS expense_date,
        '' AS description,
        e.amount,
        c.name as category_name,
        e.ID_car
    FROM expenses e
    LEFT JOIN categories c ON e.category_id = c.id
    LEFT JOIN vehicles v ON e.ID_car = v.id
    ORDER BY e.date
    """
    
    df = pd.read_sql_query(query, conn)
    
    # Сохраняем в CSV
    filename = f'expenses_with_categories_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"Таблица expenses экспортирована в файл: {filename}")
    print(f"Количество записей: {len(df)}")
    
    conn.close()
    return filename

def export_vehicles():
    """Экспорт таблицы vehicles"""
    conn = sqlite3.connect('data.db')
    
    query = "SELECT * FROM vehicles ORDER BY id"
    df = pd.read_sql_query(query, conn)
    
    # Сохраняем в CSV
    filename = f'vehicles_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    
    print(f"Таблица vehicles экспортирована в файл: {filename}")
    print(f"Количество записей: {len(df)}")
    
    conn.close()
    return filename

def show_sample_data():
    """Показать пример данных из таблиц"""
    conn = sqlite3.connect('data.db')
    
    print("\n=== Пример данных из таблицы categories ===")
    categories_df = pd.read_sql_query("SELECT * FROM categories", conn)
    print(categories_df)
    
    print("\n=== Пример данных из таблицы expenses (первые 5 записей) ===")
    expenses_df = pd.read_sql_query("SELECT * FROM expenses LIMIT 5", conn)
    print(expenses_df)
    
    print("\n=== Пример данных из таблицы vehicles ===")
    vehicles_df = pd.read_sql_query("SELECT * FROM vehicles", conn)
    print(vehicles_df)
    
    conn.close()

if __name__ == "__main__":
    print("Начинаю экспорт таблиц в CSV формат...")
    
    # Показываем пример данных
    show_sample_data()
    
    # Экспортируем таблицы
    expenses_file = export_expenses_with_categories()
    vehicles_file = export_vehicles()
    
    print(f"\n✅ Экспорт завершен!")
    print(f"📁 Файлы созданы:")
    print(f"   - {expenses_file}")
    print(f"   - {vehicles_file}")
    print(f"\n📋 В таблице expenses категории заменены на названия:")
    print("   1 -> Топливо")
    print("   2 -> Ремонт") 
    print("   3 -> Налоги")
    print("   4 -> Штрафы")
    print("   5 -> Аренда")
    print("   6 -> Амортизация")
    print("   7 -> Админ_расходы")
    print("   8 -> Логистика") 