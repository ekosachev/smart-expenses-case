# План разработки бэкенда для динамической статистики

## 1. API Endpoint для получения статистики

### Параметры запроса:
```json
{
    "start_date": "2023-01-01",  // Дата начала периода
    "end_date": "2024-03-20",    // Дата окончания периода
    "vehicle_ids": [1, 2, 3],    // Опционально: список ID машин
    "categories": [1, 2, 3],     // Опционально: список ID категорий
    "group_by": "month"          // Группировка: "day", "month", "year"
}
```

## 2. Формат ответа API

```json
{
    "total_expenses": 1500000.0,
    "expenses_by_period": {
        "2023-01": 150000.0,
        "2023-02": 160000.0,
        "2023-03": 155000.0
    },
    "expenses_by_category": {
        "Топливо": 500000.0,
        "Ремонт": 300000.0,
        "Налоги": 200000.0
    },
    "expenses_by_vehicle": {
        "A123BC": 75000.0,
        "B456DE": 85000.0
    },
    "average_expense": 5000.0,
    "max_expense": 15000.0,
    "min_expense": 1000.0,
    "budget_comparison": {
        "planned_budget": 1600000.0,
        "actual_expenses": 1500000.0,
        "budget_utilization": 93.75
    }
}
```

## 3. Примеры SQL-запросов для статистики

```sql
-- Расходы по категориям с процентом от общего
SELECT 
    c.name as category,
    SUM(e.amount) as total_amount,
    ROUND(SUM(e.amount) * 100.0 / (SELECT SUM(amount) FROM expenses), 2) as percentage
FROM expenses e
JOIN categories c ON e.category_id = c.id
GROUP BY c.name
ORDER BY total_amount DESC;

-- Сравнение с бюджетом по месяцам
SELECT 
    mb.Год,
    mb.Месяц,
    SUM(mb.Планируемый_бюджет_руб) as planned,
    SUM(mb.Фактические_расходы_руб) as actual,
    ROUND(AVG(mb.Процент_от_плана), 2) as utilization
FROM monthly_budget mb
GROUP BY mb.Год, mb.Месяц
ORDER BY mb.Год, mb.Месяц;

-- Анализ пробега и расходов
SELECT 
    v.plate_number,
    v.total_mileage,
    SUM(e.amount) as total_expenses,
    ROUND(SUM(e.amount) / v.total_mileage, 2) as cost_per_km
FROM vehicles v
JOIN expenses e ON v.id = e.ID_car
GROUP BY v.id, v.plate_number, v.total_mileage
ORDER BY cost_per_km DESC;
``` 

## 4. Формулы расчета статистики

### 4.1 Базовые метрики
```python
def calculate_basic_metrics(expenses: List[Expense]) -> dict:
    return {
        "total_expenses": sum(e.amount for e in expenses),
        "average_expense": sum(e.amount for e in expenses) / len(expenses) if expenses else 0,
        "max_expense": max(e.amount for e in expenses) if expenses else 0,
        "min_expense": min(e.amount for e in expenses) if expenses else 0
    }
```

### 4.2 Тренды и изменения
```python
def calculate_trends(expenses: List[Expense], period: str) -> dict:
    # Расчет процентного изменения
    def percentage_change(current: float, previous: float) -> float:
        return ((current - previous) / previous * 100) if previous != 0 else 0
    
    # Расчет скользящего среднего
    def moving_average(values: List[float], window: int) -> List[float]:
        return [sum(values[i:i+window])/window for i in range(len(values)-window+1)]
    
    return {
        "month_over_month": percentage_change(current_month, previous_month),
        "year_over_year": percentage_change(current_year, previous_year),
        "moving_average_3m": moving_average(monthly_expenses, 3),
        "moving_average_6m": moving_average(monthly_expenses, 6)
    }
```

### 4.3 Аномалии
```python
def detect_anomalies(expenses: List[Expense]) -> dict:
    # Z-score для определения аномалий
    def calculate_zscore(value: float, mean: float, std: float) -> float:
        return (value - mean) / std if std != 0 else 0
    
    # IQR метод для определения выбросов
    def iqr_method(values: List[float]) -> List[float]:
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return [x for x in values if x < lower_bound or x > upper_bound]
    
    return {
        "zscore_anomalies": [e for e in expenses if abs(calculate_zscore(e.amount, mean, std)) > 2],
        "iqr_anomalies": iqr_method([e.amount for e in expenses])
    }
```

### 4.4 Бюджетный анализ
```python
def analyze_budget(expenses: List[Expense], budget: float) -> dict:
    return {
        "budget_utilization": (sum(e.amount for e in expenses) / budget * 100) if budget != 0 else 0,
        "remaining_budget": budget - sum(e.amount for e in expenses),
        "projected_overspend": calculate_projection(expenses, budget)
    }
```

## 5. Подготовка данных для RAG

### 5.1 Важность структурированных данных для RAG

Для эффективной работы RAG (Retrieval-Augmented Generation) системы с финансовыми данными критически важно обеспечить правильную структуру и контекст данных. Это обусловлено следующими факторами:

1. **Качество ответов:**
   - RAG система использует структурированные данные для формирования точных и релевантных ответов
   - Чем лучше структурированы данные, тем более точные рекомендации может дать система
   - JSON формат обеспечивает четкую иерархию данных, что упрощает их обработку

2. **Преимущества JSON формата:**
   - Легкая сериализация/десериализация данных
   - Поддержка вложенных структур для сложных взаимосвязей
   - Возможность быстрой валидации через схемы
   - Удобство для машинной обработки и хранения

### 5.2 Необходимая структура данных для RAG
```json
{
    "context": {
        "time_period": {
            "start": "2024-01-01",
            "end": "2024-03-20",
            "seasonal_context": "winter",
            "holiday_periods": ["2024-01-01", "2024-01-07"]
        },
        "summary": {
            "total_expenses": 1500000.0,
            "key_trends": ["рост расходов на топливо", "снижение затрат на ремонт"],
            "anomalies": ["необычно высокий расход в феврале"],
            "budget_status": "в пределах нормы",
            "risk_level": "low",
            "optimization_potential": "medium"
        },
        "detailed_metrics": {
            "category_breakdown": {
                "fuel": {
                    "amount": 500000.0,
                    "trend": "increasing",
                    "anomalies": [],
                    "seasonal_pattern": "winter_peak",
                    "forecast": {
                        "next_month": 520000.0,
                        "confidence": 0.85
                    },
                    "optimization_suggestions": [
                        {
                            "type": "fuel_efficiency",
                            "potential_savings": 50000.0,
                            "confidence": 0.9
                        }
                    ]
                },
                "maintenance": {
                    "amount": 300000.0,
                    "trend": "decreasing",
                    "anomalies": [],
                    "maintenance_schedule": "up_to_date",
                    "predictive_maintenance": {
                        "next_service": "2024-04-15",
                        "estimated_cost": 45000.0
                    }
                }
            },
            "vehicle_metrics": {
                "A123BC": {
                    "total_expenses": 75000.0,
                    "cost_per_km": 2.5,
                    "maintenance_frequency": "normal",
                    "efficiency_score": 0.85,
                    "historical_comparison": {
                        "previous_period": 80000.0,
                        "change_percentage": -6.25
                    },
                    "predictive_metrics": {
                        "expected_lifetime": "2026-12",
                        "depreciation_rate": 0.15,
                        "maintenance_forecast": {
                            "next_3_months": 25000.0,
                            "confidence": 0.8
                        }
                    }
                }
            },
            "budget_analysis": {
                "current_period": {
                    "planned": 1600000.0,
                    "actual": 1500000.0,
                    "variance": -6.25
                },
                "forecast": {
                    "next_quarter": 1650000.0,
                    "confidence": 0.9,
                    "risk_factors": [
                        {
                            "factor": "fuel_price_increase",
                            "probability": 0.7,
                            "impact": "high"
                        }
                    ]
                }
            }
        }
    },
    "metadata": {
        "last_updated": "2024-03-20T12:00:00Z",
        "data_quality": "high",
        "confidence_scores": {
            "trend_analysis": 0.95,
            "anomaly_detection": 0.90,
            "forecast_accuracy": 0.85
        },
        "data_sources": {
            "expenses": "primary_database",
            "market_data": "external_api",
            "weather_data": "meteorological_service"
        },
        "model_parameters": {
            "forecast_horizon": "3_months",
            "update_frequency": "daily",
            "min_confidence_threshold": 0.8
        }
    },
    "recommendations_context": {
        "business_rules": [
            {
                "rule": "maintenance_threshold",
                "value": 100000.0,
                "priority": "high"
            }
        ],
        "optimization_goals": [
            {
                "goal": "reduce_fuel_costs",
                "target_reduction": 10.0,
                "timeframe": "6_months"
            }
        ],
        "constraints": [
            {
                "type": "budget_limit",
                "value": 2000000.0,
                "period": "annual"
            }
        ]
    }
}
```

### 5.3 Форматирование для RAG
```