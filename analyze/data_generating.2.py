import sqlite3
import pandas as pd
import os

def generate_monthly_budget_table_func(db_path: str = os.path.join(os.path.pardir, 'data.db')):
    conn = sqlite3.connect(db_path)
    
    # Debug: Проверка схемы таблицы expenses в начале функции
    # print("\nDebug (inside generate_monthly_budget_table_func): Проверка схемы таблицы expenses...")
    # cursor_debug = conn.cursor()
    # cursor_debug.execute("PRAGMA table_info(expenses)")
    # schema_debug = cursor_debug.fetchall()
    # if schema_debug:
    #     print("Схема таблицы expenses (изнутри функции):")
    #     for col in schema_debug:
    #         print(col)
    # else:
    #     print("Таблица expenses не найдена или пуста (изнутри функции).")
    
    # Получаем расходы по категориям 1-8 и ID_car
    query = """
    SELECT
        strftime('%Y', date) AS year,
        strftime('%m', date) AS month,
        ID_car,
        SUM(amount) AS actual_expenses_rub
    FROM expenses
    WHERE category_id BETWEEN 1 AND 8
    GROUP BY year, month, ID_car
    ORDER BY year, month, ID_car;
    """
    print(f"\nDebug: SQL-запрос для actual_expenses_df:\n{query}") # Добавлено для отладки
    
    actual_expenses_df = pd.read_sql_query(query, conn)
    
    if actual_expenses_df.empty:
        print("Нет данных для генерации ежемесячного бюджета.")
        conn.close()
        return

    # Рассчитываем средний расход на каждую машину по категориям 1-8 за весь период для планируемого бюджета
    # Это будет нашей базовой "планируемой" суммой для каждой машины в месяц
    planned_budget_base_query = """
    SELECT
        ID_car,
        AVG(amount) AS avg_monthly_amount_per_car
    FROM (
        SELECT
            strftime('%Y', date) AS year,
            strftime('%m', date) AS month,
            ID_car,
            SUM(amount) AS total_amount_per_month
        FROM expenses
        WHERE category_id BETWEEN 1 AND 8
        GROUP BY year, month, ID_car
    )
    GROUP BY ID_car;
    """
    print(f"\nDebug: SQL-запрос для planned_budget_base_df:\n{planned_budget_base_query}") # Добавлено для отладки
    planned_budget_base_df = pd.read_sql_query(planned_budget_base_query, conn)
    
    # Объединяем фактические расходы с базовыми значениями планируемого бюджета
    monthly_budget_df = pd.merge(actual_expenses_df, planned_budget_base_df, on='ID_car', how='left')
    
    # Заполняем NaN в planned_budget_rub (для машин, по которым не было данных для расчета средней)
    # используя общий средний расход по всем машинам
    overall_avg_query = """
    SELECT AVG(amount) FROM expenses WHERE category_id BETWEEN 1 AND 8;
    """
    print(f"\nDebug: SQL-запрос для overall_avg_amount:\n{overall_avg_query}") # Добавлено для отладки
    overall_avg_amount = conn.execute(overall_avg_query).fetchone()[0]
    
    monthly_budget_df['planned_budget_rub'] = monthly_budget_df['avg_monthly_amount_per_car'].fillna(overall_avg_amount)
    
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

# --- Главный блок выполнения ---
if __name__ == "__main__":
    db_file_name = 'data.db'
    db_path = os.path.join(os.path.pardir, db_file_name)

    # Удаляем базу данных перед генерацией новых данных, чтобы избежать дубликатов
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Удалена существующая база данных: {db_path}")

    print("\n--- Запуск всех операций управления данными ---")

    # Шаг 1: Генерация данных о расходах и импорт в базу данных
    print("\nШаг 1: Генерация данных о расходах...")
    generate_expenses_data_func(db_path)
    # print("Сгенерировано и сохранено в базу данных 1787 записей") # перемещено внутрь функции

    # Шаг 2: Генерация и импорт данных о транспортных средствах
    print("\nШаг 2: Генерация и импорт данных о транспортных средствах...")
    num_vehicles_to_generate = 20 # Задайте желаемое количество транспортных средств
    vehicles_data = generate_vehicles_func(num_vehicles_to_generate)
    create_vehicles_table_func(db_path) # Убедимся, что таблица vehicles создана
    import_vehicles_to_db_func(vehicles_data, db_path)
    print(f"Успешно сгенерировано и импортировано {len(vehicles_data)} транспортных средств")

    # Шаг 3: Генерация и импорт данных о пробеге
    print("\nШаг 3: Генерация и импорт данных о пробеге...")
    generate_mileage_data_func(db_path)
    print(f"Успешно сгенерировано и импортировано 16900 записей о пробеге")

    # Шаг 4: Обновление общего пробега в таблице транспорта
    print("\nШаг 4: Обновление общего пробега в таблице транспорта...")
    update_total_mileage_func(db_path)

    # Шаг 5: Генерация таблицы ежемесячного бюджета
    print("\nШаг 5: Генерация таблицы ежемесячного бюджета...")
    generate_monthly_budget_table_func(db_path=db_file_path)

    print("\n--- Все операции по управлению данными завершены ---") 