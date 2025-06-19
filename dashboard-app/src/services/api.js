const API_BASE_URL = '/api';

export const apiService = {
  // Запрос к расходам через LLM
  async queryExpenses(queryData) {
    try {
      const response = await fetch(`${API_BASE_URL}/expense_query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryData),
      });
      return await response.json();
    } catch (error) {
      console.error('Ошибка при запросе расходов:', error);
      throw error;
    }
  },

  // Получение отчета о расходах
  async getExpensesReport(queryData) {
    try {
      const response = await fetch(`${API_BASE_URL}/expense_query/report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryData),
      });
      return await response.blob();
    } catch (error) {
      console.error('Ошибка при получении отчета:', error);
      throw error;
    }
  },

  // Импорт транспортных средств
  async importVehicles(formData) {
    try {
      const response = await fetch(`${API_BASE_URL}/import/vehicles`, {
        method: 'POST',
        body: formData,
      });
      return await response.json();
    } catch (error) {
      console.error('Ошибка при импорте ТС:', error);
      throw error;
    }
  },

  // Импорт расходов
  async importExpenses(formData) {
    try {
      const response = await fetch(`${API_BASE_URL}/import/expenses`, {
        method: 'POST',
        body: formData,
      });
      return await response.json();
    } catch (error) {
      console.error('Ошибка при импорте расходов:', error);
      throw error;
    }
  },

  // Скачать шаблон для ТС
  async downloadVehiclesTemplate(format = 'xlsx') {
    try {
      const response = await fetch(`${API_BASE_URL}/import/template/vehicles?format=${format}`);
      return await response.blob();
    } catch (error) {
      console.error('Ошибка при скачивании шаблона ТС:', error);
      throw error;
    }
  },

  // Скачать шаблон для расходов
  async downloadExpensesTemplate(format = 'xlsx') {
    try {
      const response = await fetch(`${API_BASE_URL}/import/template/expenses?format=${format}`);
      return await response.blob();
    } catch (error) {
      console.error('Ошибка при скачивании шаблона расходов:', error);
      throw error;
    }
  },

  // Получение ролей пользователей
  async getRoles() {
    try {
      const response = await fetch(`${API_BASE_URL}/roles/`);
      return await response.json();
    } catch (error) {
      console.error('Ошибка при получении ролей:', error);
      throw error;
    }
  }
}; 