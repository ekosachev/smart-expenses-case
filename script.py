import json
from model import RAG_model
import os

def main():
    # Загружаем данные из JSON файла
    with open('test_data.json', 'r', encoding='utf-8') as file:
        statistics = json.load(file)
    
    # Создаем экземпляр RAG модели
    rag_model = RAG_model()
    
    # Получаем анализ расходов
    analysis = rag_model.analyze_expenses(statistics)

    print('API_LLM:', os.getenv('API_LLM'))
    print('ANALYSIS:', analysis)

    # Сохраняем результат в текстовый файлё
    #with open('expenses_analysis.txt', 'w', encoding='utf-8') as file:
        #file.write(analysis)

    with open('expenses_analysis.md', 'w', encoding='utf-8') as file:
        file.write(analysis)

if __name__ == "__main__":
    main() 