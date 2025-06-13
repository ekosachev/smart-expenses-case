import aiohttp
import asyncio
import json
import os
import dotenv
from dotenv import load_dotenv
import requests

load_dotenv()

async def invoke_chute():
    api_token = os.getenv('API_LLM')
    
    headers = {
        "Authorization": "Bearer " + api_token,
		"Content-Type": "application/json"
	}

    body = {
        "model": "deepseek-ai/DeepSeek-V3-0324",
        "messages": [
        {
            "role": "user",
            "content": "Расскажи историю 200."
        }
    ],
        "stream": True,
        "max_tokens": 1024,
        "temperature": 0.7
    }
    full_response = ''
    
    response = requests.post("https://llm.chutes.ai/v1/chat/completions", headers=headers, json=body, stream=True)
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
                pass
    print(full_response)

asyncio.run(invoke_chute())