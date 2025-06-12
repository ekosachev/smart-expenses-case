import sqlite3

def update_total_mileage():
    conn = sqlite3.connect('expenses.db')
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

if __name__ == '__main__':
    update_total_mileage() 