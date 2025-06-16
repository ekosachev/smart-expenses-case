import asyncio
import json
import os
import dotenv
from dotenv import load_dotenv
import requests
from typing import Dict, Any

class RAG_model:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv('API_LLM')
        self.base_url = "https://llm.chutes.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    
    def _create_prompt(self, statistics: Dict[str, Any]) -> str:
        prompt = """Ты - финансовый аналитик, специализирующийся на анализе расходов на транспорт. 
        Проанализируй предоставленную статистику и дай конкретные рекомендации по оптимизации расходов.
        
        Статистика расходов:
        {statistics}
        
        Пожалуйста, предоставь:
        1. Краткий анализ основных трендов
        2. 3-5 конкретных рекомендаций по оптимизации расходов
        3. Потенциальные риски и как их избежать
        4. Прогноз расходов на следующий период
        
        Формат ответа должен быть структурированным и конкретным. Категория пробег считается в километрах"""
        return prompt.format(statistics=json.dumps(statistics, indent=2, ensure_ascii=False))
    

    def analyze_expenses(self, expenses: Dict[str, Any]) -> str:

        prompt = self._create_prompt(expenses)

        messages = [
            {
                "role": "system",
                "content": "Ты - финансовый аналитик, специализирующийся на анализе расходов на транспорт."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        body = {
            "model": "deepseek-ai/DeepSeek-V3-0324",
            "messages": messages,
            "stream": True,
            "max_tokens": 1024,
            "temperature": 0.7
        }

        full_response = ''

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=body,
                stream=True
                )
            for line in response.iter_lines():
                if line:
                    try:
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            line_text = line_text[6:]
                            if line_text.strip() and line_text != '[DONE]':
                                parsed = json.loads(line_text)
                                content = parsed.get('choices', [{}])[0].get('delta', {}).get('content', '')
                                if content:
                                    full_response += content
                    except:
                        continue
            return full_response
        except Exception as e:
            return f"Ошибка при анализе расходов: {str(e)}"