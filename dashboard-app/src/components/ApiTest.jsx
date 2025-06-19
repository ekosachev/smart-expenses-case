import React, { useState } from 'react';
import { apiService } from '../services/api';

const ApiTest = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const testQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiService.queryExpenses({
        query: query,
        company_id: 1
      });
      setResult(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadTemplate = async () => {
    try {
      const blob = await apiService.downloadExpensesTemplate();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'expenses_template.xlsx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px' }}>
      <h2>Тест подключения к API</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <label>
          Запрос к расходам:
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Например: покажи расходы за последний месяц"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </label>
        <button 
          onClick={testQuery}
          disabled={loading}
          style={{ marginTop: '10px', padding: '8px 16px' }}
        >
          {loading ? 'Загрузка...' : 'Отправить запрос'}
        </button>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <button onClick={downloadTemplate}>
          Скачать шаблон расходов
        </button>
      </div>

      {error && (
        <div style={{ color: 'red', marginBottom: '20px' }}>
          Ошибка: {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Результат:</h3>
          <pre style={{ background: '#f5f5f5', padding: '10px', overflow: 'auto' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ApiTest; 