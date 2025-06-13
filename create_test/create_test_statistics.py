import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Literal, Optional, Union, Dict, List
import sqlite3
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        pass

class SQLiteDataSource(DataSource):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_data(self) -> pd.DataFrame:
        conn = sqlite3.connect(self.db_path)
        query = """
        SELECT 
            e.date as 'Дата',
            e.amount as 'Сумма',
            c.name as 'Категория'
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.id
        """
        df = pd.read_sql_query(query, conn)
        df['Дата'] = pd.to_datetime(df['Дата'])
        conn.close()
        return df

def create_data_source(source_type: str, **kwargs) -> DataSource:
    """Фабрика для создания источника данных"""
    if source_type.lower() == 'sqlite':
        return SQLiteDataSource(kwargs['db_path'])
    else:
        raise ValueError(f"Неподдерживаемый тип источника данных: {source_type}")

def filter_by_period(df: pd.DataFrame, period: Literal['3d', '7d', '30d', '365d'], end_date: Optional[str]=None) -> pd.DataFrame:
    if end_date:
        end = pd.to_datetime(end_date)
    else:
        end = df['Дата'].max()
    if period == '3d':
        start = end - timedelta(days=2)
    elif period == '7d':
        start = end - timedelta(days=6)
    elif period == '30d':
        start = end - timedelta(days=29)
    elif period == '365d':
        start = end - timedelta(days=364)
    else:
        raise ValueError('Период должен быть одним из: 3d, 7d, 30d, 365d')
    return df[(df['Дата'] >= start) & (df['Дата'] <= end)]

def calc_period_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"пусто": True}
    stats = {
        "период": {
            "начало": df['Дата'].min().strftime('%Y-%m-%d'),
            "конец": df['Дата'].max().strftime('%Y-%m-%d'),
            "количество_дней": (df['Дата'].max() - df['Дата'].min()).days + 1
        },
        "общая_сумма": float(df['Сумма'].sum()),
        "средний_расход_в_день": float(df.groupby('Дата')['Сумма'].sum().mean()),
        "медианный_расход": float(df['Сумма'].median()),
        "категории": [],
        "по_дням": []
    }
    # По категориям
    cat_stats = df.groupby('Категория')['Сумма'].agg(['count', 'sum', 'mean', 'min', 'max']).round(2)
    for cat, row in cat_stats.iterrows():
        stats['категории'].append({
            "категория": cat,
            "количество": int(row['count']),
            "сумма": float(row['sum']),
            "среднее": float(row['mean']),
            "минимум": float(row['min']),
            "максимум": float(row['max'])
        })
    # По дням
    day_stats = df.groupby('Дата')['Сумма'].sum().reset_index()
    for _, row in day_stats.iterrows():
        stats['по_дням'].append({
            "дата": row['Дата'].strftime('%Y-%m-%d'),
            "сумма": float(row['Сумма'])
        })
    return stats

def get_dashboard_statistics(
    source_type: str = 'sqlite',
    periods: List[str] = ['3d', '7d', '30d', '365d'],
    end_date: Optional[str] = None,
    **source_kwargs
) -> dict:
    """
    Получение статистики для дашборда из базы данных
    
    Args:
        source_type: Тип источника данных (пока только 'sqlite')
        periods: Список периодов для анализа
        end_date: Дата окончания периода (опционально)
        **source_kwargs: Дополнительные параметры для источника данных
            - для SQLite: db_path
    """
    data_source = create_data_source(source_type, **source_kwargs)
    df = data_source.get_data()
    
    result = {}
    for period in periods:
        filtered = filter_by_period(df, period, end_date)
        result[period] = calc_period_stats(filtered)
    return result

if __name__ == "__main__":
    # Пример использования с базой данных
    stats = get_dashboard_statistics(
        source_type='sqlite',
        db_path='data.db'
    )
    
    # Сохраняем результаты
    with open('dashboard_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)