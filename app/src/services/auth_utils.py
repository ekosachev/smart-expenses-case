from fastapi import HTTPException, Depends
from typing import Dict, Any

def get_current_user() -> Dict[str, Any]:
    """
    Простая заглушка для аутентификации пользователя.
    В реальном приложении здесь должна быть проверка токена.
    """
    # Возвращаем тестового пользователя
    return {
        "id": 1,
        "username": "test_user",
        "email": "test@example.com",
        "role": "admin"
    } 