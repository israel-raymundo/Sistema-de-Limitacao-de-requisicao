import time
import threading

class RateLimiter:
    def __init__(self, max_tokens: int = 5, refill_rate: float = 1.0):
        """
        max_tokens  → máximo de requisições permitidas por janela
        refill_rate → quantos tokens são adicionados por segundo
        """
        self.max_tokens  = max_tokens
        self.refill_rate = refill_rate
        self.users       = {}         # guarda o estado de cada usuário
        self.lock        = threading.Lock()  # evita conflito entre threads

    def _get_user(self, user_id: str) -> dict:
        """Retorna o balde do usuário, criando um novo se não existir."""
        if user_id not in self.users:
            self.users[user_id] = {
                "tokens":      self.max_tokens,
                "last_refill": time.time()
            }
        return self.users[user_id]

    def _refill(self, user: dict):
        """
        Reabastece os tokens com base no tempo passado desde o último refill.
        Se passou 2 segundos e a taxa é 1 token/segundo → adiciona 2 tokens.
        """
        agora          = time.time()
        tempo_passado  = agora - user["last_refill"]
        novos_tokens   = tempo_passado * self.refill_rate

        user["tokens"]      = min(self.max_tokens, user["tokens"] + novos_tokens)
        user["last_refill"] = agora

    def allow(self, user_id: str) -> dict:
        """
        Verifica se a requisição do usuário pode passar.
        Retorna um dicionário com o resultado e informações do estado atual.
        """
        with self.lock:
            user = self._get_user(user_id)
            self._refill(user)

            if user["tokens"] >= 1:
                user["tokens"] -= 1
                return {
                    "allowed":    True,
                    "tokens":     int(user["tokens"]),
                    "max_tokens": self.max_tokens,
                    "message":    "✅ Requisição aceita"
                }
            else:
                return {
                    "allowed":    False,
                    "tokens":     0,
                    "max_tokens": self.max_tokens,
                    "message":    "Limite atingido! Tente novamente em instantes."
                }

    def status(self) -> dict:
        """Retorna o estado atual de todos os usuários."""
        return {
            uid: {
                "tokens":   int(u["tokens"]),
                "max":      self.max_tokens
            }
            for uid, u in self.users.items()
        }