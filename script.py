import json
from model import RAG_model

def main():
    # Загружаем данные из JSON файла
    with open('test_data.json', 'r', encoding='utf-8') as file:
        statistics = json.load(file)
    
    # Создаем экземпляр RAG модели
    rag_model = RAG_model()
    
    # Получаем анализ расходов
    analysis = rag_model.analyze_expenses(statistics)
    
    # Сохраняем результат в текстовый файл
    with open('expenses_analysis.md', 'w', encoding='utf-8') as file:
        file.write(analysis)

if __name__ == "__main__":
    main() 