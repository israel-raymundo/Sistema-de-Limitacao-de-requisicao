# 🛡️ Rate Limiter — Token Bucket

Sistema de limitação de requisições desenvolvido em Python com Flask,
usando o algoritmo Token Bucket para proteger servidores contra
sobrecarga e ataques de força bruta.

## 💼 Valor para empresas
APIs e sistemas web sem proteção ficam vulneráveis a sobrecarga
por excesso de requisições — seja por ataque ou por pico de acesso.
O Rate Limiter garante que cada usuário tenha acesso justo ao
servidor, protegendo a estabilidade do sistema sem derrubar o
serviço para todos.

## 🚀 Como usar

1. Clone o repositório
2. Instale as dependências:
pip install flask
3. Execute:
python app.py
4. Acesse: http://127.0.0.1:5000

## ✨ Funcionalidades
- Algoritmo Token Bucket por usuário
- Dashboard visual com barras de tokens em tempo real
- Log de requisições com HTTP 200 e HTTP 429
- Simulação de sobrecarga com 10 requisições simultâneas
- Suporte a múltiplos usuários independentes

## 🧠 Como funciona
Cada usuário tem um balde com 5 tokens. Cada requisição consome
1 token. O balde é reabastecido em 1 token por segundo. Se o balde
estiver vazio, a requisição é bloqueada com erro 429.

## 🛠️ Tecnologias
- Python 3.8+
- Flask — framework web
- Threading — controle de concorrência
