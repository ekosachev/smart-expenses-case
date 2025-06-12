import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_expenses_data():
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

    data = []
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
                data.append([
                    id_counter,
                    vehicle,
                    category,
                    round(amount),
                    date.strftime('%Y-%m-%d')
                ])
                id_counter += 1

    df = pd.DataFrame(data, columns=['ID', 'Автомобиль', 'Категория', 'Сумма', 'Дата'])

    
    return df

if __name__ == "__main__":
    df = generate_expenses_data()
    df.to_csv("expenses.csv", index=False)
    print(f"Сгенерировано {len(df)} записей и сохранено в expenses.csv") 