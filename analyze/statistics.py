import pandas as pd
import numpy as np
from datetime import datetime
import json

def calculate_statistics():
    df = pd.read_csv("expenses.csv")
    df['Дата'] = pd.to_datetime(df['Дата'])
    df['Месяц'] = df['Дата'].dt.month
    df['Год'] = df['Дата'].dt.year
    df['День недели'] = df['Дата'].dt.day_name()
    
    # Основная структура для JSON
    stats = {
        "общая_информация": {
            "всего_записей": int(len(df)),
            "период": {
                "начало": df['Дата'].min().strftime('%Y-%m-%d'),
                "конец": df['Дата'].max().strftime('%Y-%m-%d'),
                "дней_в_периоде": (df['Дата'].max() - df['Дата'].min()).days
            },
            "общая_сумма_расходов": float(df['Сумма'].sum()),
            "средний_расход_в_день": float(df['Сумма'].mean()),
            "медианный_расход": float(df['Сумма'].median())
        },
        
        "категории": {
            "статистика_по_категориям": [],
            "распределение_расходов": {},
            "динамика_по_категориям": {}
        },
        
        "временной_анализ": {
            "по_месяцам": [],
            "по_дням_недели": [],
            "тренды": {
                "месячный_рост": float(0),
                "сезонность": {}
            }
        },
        
        "выбросы": {
            "обнаружены": False,
            "количество": 0,
            "сумма_выбросов": 0,
            "процент_от_общих_расходов": 0
        }
    }
    
    # Статистика по категориям
    category_stats = df.groupby('Категория').agg({
        'Сумма': ['count', 'sum', 'mean', 'median', 'min', 'max', 'std']
    }).round(2)
    
    for category in category_stats.index:
        cat_data = category_stats.loc[category]
        stats["категории"]["статистика_по_категориям"].append({
            "категория": category,
            "количество_транзакций": int(cat_data[('Сумма', 'count')]),
            "общая_сумма": float(cat_data[('Сумма', 'sum')]),
            "средняя_сумма": float(cat_data[('Сумма', 'mean')]),
            "медианная_сумма": float(cat_data[('Сумма', 'median')]),
            "минимальная_сумма": float(cat_data[('Сумма', 'min')]),
            "максимальная_сумма": float(cat_data[('Сумма', 'max')]),
            "стандартное_отклонение": float(cat_data[('Сумма', 'std')])
        })
        
        # Распределение расходов по категориям
        stats["категории"]["распределение_расходов"][category] = float(
            cat_data[('Сумма', 'sum')] / df['Сумма'].sum() * 100
        )
    
    # Временной анализ
    monthly_stats = df.groupby(['Год', 'Месяц']).agg({
        'Сумма': ['sum', 'mean', 'count']
    }).round(2)
    
    for (year, month), data in monthly_stats.iterrows():
        stats["временной_анализ"]["по_месяцам"].append({
            "год": int(year),
            "месяц": int(month),
            "общая_сумма": float(data[('Сумма', 'sum')]),
            "средняя_сумма": float(data[('Сумма', 'mean')]),
            "количество_транзакций": int(data[('Сумма', 'count')])
        })
    
    # Анализ по дням недели
    weekday_stats = df.groupby('День недели')['Сумма'].agg(['sum', 'mean', 'count']).round(2)
    for day, data in weekday_stats.iterrows():
        stats["временной_анализ"]["по_дням_недели"].append({
            "день": day,
            "общая_сумма": float(data['sum']),
            "средняя_сумма": float(data['mean']),
            "количество_транзакций": int(data['count'])
        })
    
    # Анализ выбросов
    mean_by_month = df.groupby(['Год', 'Месяц'])['Сумма'].mean()
    std_by_month = df.groupby(['Год', 'Месяц'])['Сумма'].std()
    outliers = []
    
    for (year, month), mean in mean_by_month.items():
        std = std_by_month[(year, month)]
        threshold = mean + 2 * std
        month_outliers = df[
            (df['Год'] == year) & 
            (df['Месяц'] == month) & 
            (df['Сумма'] > threshold)
        ]
        if not month_outliers.empty:
            outliers.append(month_outliers)
    
    if outliers:
        outliers_df = pd.concat(outliers)
        stats["выбросы"]["обнаружены"] = True
        stats["выбросы"]["количество"] = len(outliers_df)
        stats["выбросы"]["сумма_выбросов"] = float(outliers_df['Сумма'].sum())
        stats["выбросы"]["процент_от_общих_расходов"] = float(
            outliers_df['Сумма'].sum() / df['Сумма'].sum() * 100
        )
        # Сохраняем выбросы в CSV
        outliers_df.to_csv('expenses_outliers.csv', index=False)
    
    # Сохраняем всю статистику в JSON
    with open('expenses_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    calculate_statistics() 