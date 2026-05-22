from flask import Flask, render_template, request, jsonify  #jsonify converte dicionário Python em JSON para o navegador entender
from rate_limiter import RateLimiter

app = Flask(__name__)

# Criando o Rate Limiter com 5 tokens máximos e 1 token por segundo
limiter = RateLimiter(max_tokens=5, refill_rate=1.0)

# ─── DASHBOARD ───────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─── SIMULAR REQUISIÇÃO ──────────────────────────────────
@app.route("/requisicao", methods=["POST"])
def requisicao():
    """
    Recebe uma requisição de um usuário e verifica se pode passar.
    O user_id identifica quem está fazendo a requisição.
    """
    data    = request.get_json()
    user_id = data.get("user_id", "usuario_1")
    result  = limiter.allow(user_id)

    # Retorna 200 se aceito, 429 se bloqueado
    status_code = 200 if result["allowed"] else 429  #código HTTP padrão para "Too Many Requests"
    return jsonify(result), status_code

# ─── STATUS GERAL ────────────────────────────────────────
@app.route("/status")
def status():
    """Retorna o estado atual do balde de todos os usuários."""
    return jsonify(limiter.status())

# ─── RESETAR ─────────────────────────────────────────────
@app.route("/resetar")
def resetar():
    """Reseta todos os usuários para testar novamente."""
    limiter.users = {}
    return jsonify({"message": "✅ Rate Limiter resetado!"})

if __name__ == "__main__":
    app.run(debug=True)