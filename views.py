from main import app
from flask import render_template, request, jsonify
from chatbot import responder

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/chat", methods=["POST"])
def chat():
    mensagem = request.json["mensagem"]

    if mensagem.lower() == "sair":
        return jsonify({"resposta": "Até mais! 👋"})

    resposta = responder(mensagem)
    return jsonify({"resposta": resposta})