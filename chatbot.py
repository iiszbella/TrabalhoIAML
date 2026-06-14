"""Chatbot de jogos de horror com NLTK, memória de conversa e fluxo reativo."""

import random
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
from hooks import JOGOS, GENEROS, NOMES_ALT, SIM, NAO, CONVERSA_PROFUNDA
from rawg_service import buscar_jogo_api
from llm_service import responder_llm

# Baixa recursos NLTK necessários
for _r in ['punkt_tab', 'rslp']:
    nltk.download(_r, quiet=True)

stemmer = RSLPStemmer()

# Stems pré-computados para detectar intenções
_STEMS_RECOMENDACAO = {stemmer.stem(p) for p in ['recomend', 'suger', 'indic']}
_STEMS_IDENTIDADE = {stemmer.stem(p) for p in ['nom', 'cham']}

# ================================================================
# FUNÇÕES DE NLP
# ================================================================

def normalizar(texto):
    """Remove acentos e normaliza para minúsculas."""
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def tokenizar(texto):
    """Tokeniza e aplica stemming com NLTK."""
    tokens = word_tokenize(normalizar(texto), language='portuguese')
    return tokens, [stemmer.stem(t) for t in tokens]


def detectar_jogo(texto):
    """Detecta qual jogo foi mencionado no texto usando nomes, aliases e tags."""
    texto_n = normalizar(texto)

    # 1) Nome completo (mais longo primeiro para evitar match parcial)
    for nome in sorted(JOGOS, key=len, reverse=True):
        if normalizar(nome) in texto_n:
            return nome

    # 2) Aliases
    for alt in sorted(NOMES_ALT, key=len, reverse=True):
        if normalizar(alt) in texto_n:
            return NOMES_ALT[alt]

    # 3) Tags (pontua por nº de matches e pega o melhor)
    tokens = set(texto_n.split())
    melhor, score = None, 0
    for nome, dados in JOGOS.items():
        s = sum(1 for t in dados['tags'] if t in tokens or t in texto_n)
        if s > score:
            melhor, score = nome, s
    return melhor if score > 0 else None


def detectar_genero(texto):
    """Detecta gênero de horror mencionado no texto."""
    texto_n = normalizar(texto)
    mapa = {
        'survival': 'survival horror', 'sobrevivencia': 'survival horror',
        'psicologico': 'terror psicológico', 'mental': 'terror psicológico',
        'jump': 'jump scare', 'susto': 'jump scare', 'jumpscare': 'jump scare',
        'acao': 'ação', 'combate': 'ação',
        'narrativo': 'narrativo', 'escolha': 'narrativo', 'interativo': 'narrativo',
        'multiplayer': 'multiplayer', 'online': 'multiplayer',
        'ficcao': 'ficção científica', 'espaco': 'ficção científica',
    }
    for chave, genero in mapa.items():
        if chave in texto_n:
            return genero
    return None


def eh_sim(texto):
    n = normalizar(texto)
    return n in SIM or any(t in SIM for t in n.split())


def eh_nao(texto):
    n = normalizar(texto)
    return n in NAO or any(t in NAO for t in n.split())


def _eh_saudacao(texto):
    n = normalizar(texto)
    tokens = n.split()
    palavras = {'oi', 'ola', 'eai', 'opa', 'fala', 'salve', 'hey', 'oie', 'hello',
                'hi', 'yo', 'ae', 'iae', 'eae'}
    if any(t in palavras for t in tokens):
        return True
    frases = ['bom dia', 'boa tarde', 'boa noite', 'e ai', 'e ae']
    return any(f in n for f in frases)


def _eh_despedida(texto):
    return any(t in {'tchau', 'adeus', 'bye', 'sair', 'vlw', 'valeu', 'obrigado', 'obg', 'flw'}
               for t in normalizar(texto).split())


def _quer_trocar(texto):
    """Detecta se o usuário quer mudar de assunto ou parar a conversa atual."""
    n = normalizar(texto)
    return any(p in n for p in [
        'trocar', 'mudar', 'outro assunto', 'chega', 'parar',
        'cansei', 'enjoei', 'outro jogo', 'outra coisa', 'basta',
        'proximo', 'next', 'pular',
    ])


# ================================================================
# MEMÓRIA DE CONVERSA
# ================================================================

class Memoria:
    def __init__(self):
        self.estado = None          
        self.ultimo_jogo = None     
        self.jogo_sugerido = None   
        self.pergunta_idx = 0       
        self.historico = []         

    def salvar(self, user, bot):
        self.historico.append({'user': user, 'bot': bot})


memoria = Memoria()

# ================================================================
# RESPONDER — FUNÇÃO PRINCIPAL COM INDICADOR DE FONTE
# ================================================================

def responder(mensagem):
    jogo = detectar_jogo(mensagem)

    if jogo:
        dados_jogo = buscar_jogo_api(jogo)

        if dados_jogo:
            # Se encontrou na API, retorna a resposta da LLM e avisa a fonte
            resposta = responder_llm(mensagem, dados_jogo)
            return {
                "texto": resposta,
                "fonte": "API (RAWG) + LLM"
            }

    # Se não identificou jogo ou a API falhou/não achou, usa apenas o conhecimento interno
    resposta = responder_llm(mensagem)
    return {
        "texto": resposta,
        "fonte": "Memória Interna (Qwen LLM)"
    }

def _processar_pendente(texto):
    # O restante da lógica de conversa profunda permanece igual
    estado = memoria.estado
    jogo_mencionado = detectar_jogo(texto)
    if jogo_mencionado:
        memoria.estado = None
        return responder(texto)

    if estado == 'curtiu_jogo':
        if eh_sim(texto):
            jogo = memoria.ultimo_jogo
            if jogo in CONVERSA_PROFUNDA:
                return _iniciar_conversa_profunda(jogo, texto)
            similares = JOGOS[jogo]['similares']
            sugerido = random.choice(similares)
            memoria.jogo_sugerido = sugerido
            memoria.estado = 'quer_similar'
            genero = JOGOS[jogo]['genero']
            r = f"Show! Já que curte {genero}, recomendo {sugerido.title()}! Quer saber mais sobre ele?"
        elif eh_nao(texto):
            r = _tratar_negacao(texto)
            if r:
                return r
            memoria.estado = 'quer_genero'
            r = "De boa! Qual gênero te interessa? Survival horror, terror psicológico, jump scare, ação ou narrativo?"
        else:
            memoria.estado = None
            return responder(texto)

    elif estado == 'conversa_profunda':
        return _avancar_conversa_profunda(texto)

    elif estado == 'quer_similar':
        if eh_sim(texto) and memoria.jogo_sugerido in JOGOS:
            jogo = memoria.jogo_sugerido
            info = random.choice(JOGOS[jogo]['info'])
            memoria.ultimo_jogo = jogo
            memoria.estado = 'curtiu_jogo'
            r = f"{info}\n\nCurtiu {jogo.title()}?"
        elif eh_nao(texto):
            r = _tratar_negacao(texto)
            if r:
                return r
            memoria.estado = 'quer_genero'
            r = "Tranquilo! Me fala que tipo de terror você curte!"
        else:
            memoria.estado = None
            return responder(texto)

    elif estado == 'quer_genero':
        genero = detectar_genero(texto)
        if genero and genero in GENEROS:
            jogos = ', '.join(GENEROS[genero])
            memoria.estado = 'quer_detalhe'
            r = f"Pra {genero}, recomendo: {jogos}! Quer saber sobre algum?"
        else:
            r = "Não reconheci! Tenta: survival horror, terror psicológico, jump scare, ação, narrativo ou ficção científica."

    elif estado == 'quer_detalhe':
        if eh_sim(texto):
            r = "Legal! Me diz qual deles você quer conhecer! 👻"
            memoria.estado = None
        elif eh_nao(texto):
            r = "De boa! Se quiser falar sobre qualquer jogo de horror, é só mandar! 🎮"
            memoria.estado = None
        else:
            memoria.estado = None
            return responder(texto)

    elif estado == 'quer_recomendacao':
        if eh_sim(texto):
            memoria.estado = 'quer_genero'
            r = "Qual gênero te interessa? Survival horror, terror psicológico, jump scare, ação, narrativo ou ficção científica?"
        elif eh_nao(texto):
            r = "Sem problemas! Fala sobre qualquer jogo de horror! 👻"
            memoria.estado = None
        else:
            memoria.estado = None
            return responder(texto)

    else:
        memoria.estado = None
        return responder(texto)

    memoria.salvar(texto, r)
    return r

# ================================================================
# CONVERSA PROFUNDA
# ================================================================

def _iniciar_conversa_profunda(jogo, texto):
    memoria.ultimo_jogo = jogo
    memoria.pergunta_idx = 0
    memoria.estado = 'conversa_profunda'
    pergunta, _, _ = CONVERSA_PROFUNDA[jogo][0]
    r = f"Massa que curte {jogo.title()}! Bora conversar sobre ele! 🎮\n\n{pergunta}"
    memoria.salvar(texto, r)
    return r


def _avancar_conversa_profunda(texto):
    if _quer_trocar(texto):
        jogo = memoria.ultimo_jogo
        memoria.estado = None
        memoria.pergunta_idx = 0
        r = f"Sem problema! Foi bom conversar sobre {jogo.title()}. 😄 Sobre qual jogo ou gênero quer falar agora?"
        memoria.salvar(texto, r)
        return r

    jogo = memoria.ultimo_jogo
    perguntas = CONVERSA_PROFUNDA[jogo]
    idx = memoria.pergunta_idx

    _, resp_sim, resp_nao = perguntas[idx]
    if eh_nao(texto):
        comentario = resp_nao
    else:
        comentario = resp_sim

    memoria.pergunta_idx = idx + 1

    if memoria.pergunta_idx < len(perguntas):
        proxima, _, _ = perguntas[memoria.pergunta_idx]
        r = f"{comentario}\n\n{proxima}"
    else:
        similares = JOGOS[jogo]['similares']
        sugerido = random.choice(similares)
        memoria.jogo_sugerido = sugerido
        memoria.estado = 'quer_similar'
        r = f"{comentario}\n\nFoi ótimo conversar sobre {jogo.title()}! 😄 Se curte esse estilo, recomendo {sugerido.title()}. Quer saber mais?"
        memoria.salvar(texto, r)
        return r

    memoria.salvar(texto, r)
    return r


def _tratar_negacao(texto):
    jogo = detectar_jogo(texto)
    if jogo:
        memoria.estado = None
        return responder(texto)
    genero = detectar_genero(texto)
    if genero and genero in GENEROS:
        jogos = ', '.join(GENEROS[genero])
        memoria.estado = 'quer_detalhe'
        r = f"Pra {genero}, recomendo: {jogos}! Quer saber sobre algum?"
        memoria.salvar(texto, r)
        return r
    return None


def obter_saudacao_inicial():
    return random.choice([
        "Bem-vindo ao mundo do horror! 👻🎮",
        "Olá, aventureiro! Pronto pra conhecer jogos assustadores?",
        "E aí! Eu sou o Davy Jones, seu guia nos games de horror. 😱",
        "Prepare-se para o terror... sou o Davy Jones e sei tudo sobre jogos de horror! 👻",
        "Olá! Entraste nas profundezas do horror digital. Vamos explorar juntos? 🎮",
        "Bem-vindo, corajoso! Aqui a gente fala só de jogos que tiram o sono. 😈",
    ])