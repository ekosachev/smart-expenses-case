import pandas as pd
import sqlite3
import json
import os
from typing import Optional

def import_csv_to_db(csv_path: str, db_path: str = 'expenses.db'):
    df = pd.read_csv(csv_path)
    _import_df_to_db(df, db_path)

def import_json_to_db(json_path: str, db_path: str = 'expenses.db'):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    _import_df_to_db(df, db_path)

def _import_df_to_db(df: pd.DataFrame, db_path: str):
    required = {'Дата', 'Сумма', 'Категория'}
    if not required.issubset(df.columns):
        raise ValueError(f'В файле должны быть колонки: {required}')
    
    categories = df['Категория'].dropna().unique()
    cat_df = pd.DataFrame({'name': categories})
    cat_df['id'] = range(1, len(cat_df) + 1)
    
    cat_map = dict(zip(cat_df['name'], cat_df['id']))
    df['category_id'] = df['Категория'].map(cat_map)
    
    expenses_df = pd.DataFrame({
        'date': pd.to_datetime(df['Дата']).dt.strftime('%Y-%m-%d'),
        'amount': df['Сумма'],
        'category_id': df['category_id'],
        'description': df['Описание'] if 'Описание' in df.columns else None
    })
    
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Создаем таблицы
    cur.execute('''CREATE TABLE categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )''')
    cur.execute('''CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category_id INTEGER,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')
    
    cat_df[['id', 'name']].to_sql('categories', conn, if_exists='append', index=False)
    expenses_df.to_sql('expenses', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print(f'Данные успешно импортированы в {db_path}')

if __name__ == '__main__':
    import_csv_to_db('expenses.csv')
    # import_json_to_db('expenses.json') 