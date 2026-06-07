import requests

API_KEY = "676a697647c44d9e942708e555cca2c9"

def buscar_jogo_api(nome):
    url = "https://api.rawg.io/api/games"

    params = {
        "key": API_KEY,
        "search": nome
    }

    try:
        resposta = requests.get(
            url,
            params=params,
            timeout=10
        )

        resposta.raise_for_status()

        dados = resposta.json()

        if not dados.get("results"):
            return None

        jogo = dados["results"][0]

        return {
            "nome": jogo.get("name"),
            "nota": jogo.get("rating"),
            "metacritic": jogo.get("metacritic"),
            "lancamento": jogo.get("released"),
            "plataformas": [
                p["platform"]["name"]
                for p in jogo.get("platforms", [])
            ]
        }

    except Exception as erro:
        print("Erro RAWG:", erro)
        return None