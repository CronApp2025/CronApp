from datetime import datetime
from typing import Dict, Set
import threading
import time

class TokenManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.blacklisted_tokens: Set[str] = set()
                cls._instance.refresh_tokens: Dict[str, str] = {}
                cleanup_thread = threading.Thread(target=cls._instance._cleanup_expired_tokens, daemon=True)
                cleanup_thread.start()
            return cls._instance

    def add_to_blacklist(self, jti: str):
        if jti:
            with self._lock:
                self.blacklisted_tokens.add(jti)

    def is_blacklisted(self, jti: str | None) -> bool:
        if not jti or not isinstance(jti, str):
            return False
        with self._lock:
            return jti in self.blacklisted_tokens

    def store_refresh_token(self, user_id: str, refresh_token: str):
        if user_id and refresh_token:
            with self._lock:
                self.refresh_tokens[user_id] = refresh_token

    def validate_refresh_token(self, user_id: str, token: str) -> bool:
        with self._lock:
            stored_token = self.refresh_tokens.get(user_id)
            return stored_token == token if stored_token and token else False

    def remove_refresh_token(self, user_id: str):
        with self._lock:
            if user_id in self.refresh_tokens:
                self.refresh_tokens.pop(user_id)

    def _cleanup_expired_tokens(self):
        while True:
            time.sleep(3600)  # Limpiar cada hora
            with self._lock:
                self.blacklisted_tokens.clear()

token_manager = TokenManager()