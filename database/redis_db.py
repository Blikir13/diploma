import redis
import json
from datetime import datetime


class RedisMemoryManager:
    def __init__(self, host="localhost", port=6379, db=0, ttl=2400):  # 2400 сек = 40 мин
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.ttl = ttl  # TTL для каждой сессии

    def add_message(self, user_id, message):
        """Добавляет сообщение в контекст пользователя и обновляет TTL"""
        key = f"user_session:{user_id}"

        # Загружаем текущую историю диалога
        history = self.get_history(user_id)

        # Добавляем новое сообщение
        history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message
        })

        # Сохраняем обновлённую историю
        self.redis_client.set(key, json.dumps(history), ex=self.ttl)

    def get_history(self, user_id):
        """Получает историю диалога пользователя"""
        key = f"user_session:{user_id}"
        data = self.redis_client.get(key)
        return json.loads(data) if data else []

    def clear_session(self, user_id):
        """Удаляет историю пользователя"""
        key = f"user_session:{user_id}"
        self.redis_client.delete(key)

    def is_session_active(self, user_id):
        """Проверяет, активна ли сессия"""
        key = f"user_session:{user_id}"
        return self.redis_client.exists(key) > 0
