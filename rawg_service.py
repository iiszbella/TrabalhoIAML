import requests
import logging

API_KEY = "676a697647c44d9e942708e555cca2c9"
logger = logging.getLogger(__name__)

def buscar_jogo_api(nome):
    """Busca jogo na RAWG e retorna dados completos incluindo descrição limpa"""
    url = "https://api.rawg.io/api/games"

    # REMOVIDO o "search_exact" e aumentado o page_size para 25
    params = {
        "key": API_KEY,
        "search": nome,
        "page_size": 25 
    }

    try:
        resposta = requests.get(url, params=params, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        resultados = dados.get("results")
        if not resultados:
            return None

        termo_busca = nome.lower().strip()
        jogo_escolhido = None
        match_exato = True

        # 1. Correspondência Perfeita
        for jogo in resultados:
            if jogo.get("name", "").lower() == termo_busca:
                jogo_escolhido = jogo
                break
        
        # 2. Correspondência de Substring (Ex: "resident evil 9" DENTRO de "Resident Evil 9: Requiem")
        if not jogo_escolhido:
            for jogo in resultados:
                if termo_busca in jogo.get("name", "").lower():
                    jogo_escolhido = jogo
                    break

        # 3. Correspondência de Palavras (Ex: "resident", "evil", "requiem")
        if not jogo_escolhido:
            palavras_busca = termo_busca.split()
            for jogo in resultados:
                nome_jogo = jogo.get("name", "").lower()
                if all(palavra in nome_jogo for palavra in palavras_busca):
                    jogo_escolhido = jogo
                    break
        
        # 4. Fallback (Pega o mais popular, mas avisa a LLM que a busca falhou no match perfeito)
        if not jogo_escolhido:
            jogo_escolhido = resultados[0]
            match_exato = False

        jogo_id = jogo_escolhido.get("id")

        if jogo_id:
            url_detalhe = f"https://api.rawg.io/api/games/{jogo_id}"
            resposta_detalhe = requests.get(url_detalhe, params={"key": API_KEY}, timeout=10)
            resposta_detalhe.raise_for_status()
            jogo_completo = resposta_detalhe.json()
        else:
            jogo_completo = jogo_escolhido

        descricao = jogo_completo.get("description_raw")
        if not descricao:
            descricao = jogo_completo.get("description", "Descrição não disponível.")

        return {
            "nome": jogo_completo.get("name"),
            "nota": jogo_completo.get("rating"),
            "metacritic": jogo_completo.get("metacritic", "N/A"),
            "lancamento": jogo_completo.get("released", "Data desconhecida"),
            "generos": [g["name"] for g in jogo_completo.get("genres", [])],
            "descricao": descricao,
            "plataformas": [p["platform"]["name"] for p in jogo_completo.get("platforms", [])],
            "match_exato": match_exato,
            "termo_buscado": nome
        }

    except Exception as erro:
        logger.error("Erro RAWG: %s", erro)
        return None