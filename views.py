from flask import render_template, request, jsonify
from main import app
from chatbot import responder, obter_saudacao_inicial

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/saudacao", methods=["GET"])
def saudacao():
    """Retorna a saudação inicial com instruções"""
    saudacao_msg = obter_saudacao_inicial()
    instrucoes = "\n\n📚 Aqui você pode conversar sobre:\n• Jogos de Horror (Resident Evil, Silent Hill, FNAF, etc)\n• Gêneros: Survival Horror, Terror Psicológico, Jump Scare\n• Recomendações de jogos\n• Histórias e Lore de jogos assustadores\n\nComece perguntando sobre seu jogo favorito! 👻"
    
    return jsonify({
        "mensagem": saudacao_msg + instrucoes,
        "fonte": "Sistema"
    })

@app.route("/chat", methods=["POST"])
def chat():
    mensagem = request.json["mensagem"]

    if mensagem.lower() == "sair":
        return jsonify({
            "resposta": "Até mais! 👋", 
            "fonte": "Sistema"
        })

    # Agora 'resultado' recebe o dicionário com 'texto' e 'fonte'
    resultado = responder(mensagem)
    
    # Previne erros caso a função retorne apenas string em algum cenário
    if isinstance(resultado, dict):
        return jsonify({
            "resposta": resultado["texto"],
            "fonte": resultado["fonte"]
        })
    else:
        return jsonify({
            "resposta": resultado,
            "fonte": "Sistema"
        })