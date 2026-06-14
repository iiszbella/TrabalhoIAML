"""Chatbot de jogos de horror com NLTK, memória de conversa e fluxo reativo."""

import random
import logging
import unicodedata
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer

from hooks import JOGOS, GENEROS, NOMES_ALT, SIM, NAO, CONVERSA_PROFUNDA
from rawg_service import buscar_jogo_api
from llm_service import responder_llm

for _r in ['punkt_tab', 'rslp']:
    nltk.download(_r, quiet=True)

stemmer = RSLPStemmer()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================================================
# FUNÇÕES DE NLP E EXTRAÇÃO
# ================================================================

def extrair_termo_busca(mensagem):
    """Extrai de forma inteligente o nome do jogo para a API."""
    texto_lower = mensagem.lower()
    
    padroes = [
        r'(?:nota do|nota da|nota de|avaliação do|avaliação da)\s+(.+)',
        r'(?:sobre o jogo|sobre o|conhece o|conhece a|fale sobre|me fale sobre)\s+(.+)',
        r'(?:história do|história da|história de|lore do|lore de)\s+(.+)',
        r'(?:lançamento do|lançamento de)\s+(.+)',
        r'jogo\s+(.+)'
    ]
    
    for padrao in padroes:
        match = re.search(padrao, texto_lower)
        if match:
            termo = match.group(1)
            termo = re.sub(r'[?!.,]', '', termo).strip()
            termo = re.sub(r'\s+(é bom|já jogou|foi bom|vale a pena|me fale|acha|tem).*$', '', termo).strip()
            if len(termo) > 2:
                return termo
                
    for nome in sorted(JOGOS.keys(), key=len, reverse=True):
        if nome in texto_lower:
            padrao_extensao = rf"({nome}(?:\s+[a-z0-9]+){{0,2}})"
            match = re.search(padrao_extensao, texto_lower)
            if match:
                termo = match.group(1).strip()
                return re.sub(r'[?!.,]', '', termo).strip()
    
    for alt in sorted(NOMES_ALT.keys(), key=len, reverse=True):
        if alt in texto_lower:
            padrao_extensao = rf"({alt}(?:\s+[a-z0-9]+){{0,2}})"
            match = re.search(padrao_extensao, texto_lower)
            if match:
                termo = match.group(1).strip()
                return re.sub(r'[?!.,]', '', termo).strip()
                
    # O FALLBACK FOI REMOVIDO DAQUI! 
    # Agora, se não for uma pergunta de jogo, ele não trava a API e responde na hora!
    return None

def normalizar(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()

def detectar_jogo(texto):
    texto_n = normalizar(texto)
    for nome in sorted(JOGOS, key=len, reverse=True):
        if normalizar(nome) in texto_n: return nome
    for alt in sorted(NOMES_ALT, key=len, reverse=True):
        if normalizar(alt) in texto_n: return NOMES_ALT[alt]
    return None

def detectar_genero(texto):
    texto_n = normalizar(texto)
    mapa = {
        'survival': 'survival horror', 'sobrevivencia': 'survival horror',
        'psicologico': 'terror psicológico', 'mental': 'terror psicológico',
        'jump': 'jump scare', 'susto': 'jump scare',
        'acao': 'ação', 'combate': 'ação',
        'narrativo': 'narrativo', 'escolha': 'narrativo',
        'multiplayer': 'multiplayer', 'online': 'multiplayer',
        'ficcao': 'ficção científica', 'espaco': 'ficção científica',
    }
    for chave, genero in mapa.items():
        if chave in texto_n: return genero
    return None

def eh_sim(texto): return normalizar(texto) in SIM or any(t in SIM for t in normalizar(texto).split())
def eh_nao(texto): return normalizar(texto) in NAO or any(t in NAO for t in normalizar(texto).split())

def _quer_trocar(texto):
    return any(p in normalizar(texto) for p in ['trocar', 'mudar', 'outro assunto', 'chega', 'parar', 'cansei', 'enjoei', 'outro jogo', 'proximo', 'pular'])

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
# RESPONDER PRINCIPAL (Com Histórico Embutido)
# ================================================================

def responder(mensagem):
    jogo_mencionado = detectar_jogo(mensagem)
    if jogo_mencionado:
        memoria.ultimo_jogo = jogo_mencionado
        
    contexto_recomendacao = ""
    if memoria.ultimo_jogo and memoria.ultimo_jogo in JOGOS:
        dados_memoria = JOGOS[memoria.ultimo_jogo]
        similares = ", ".join([s.title() for s in dados_memoria['similares']])
        contexto_recomendacao = f"O usuário demonstrou interesse no jogo '{memoria.ultimo_jogo.title()}' (Gênero: {dados_memoria['genero']}). Se ele pedir uma recomendação ou quiser trocar de assunto, você DEVE recomendar fortemente os seguintes jogos de estilo similar: {similares}."

    # PEGA AS ÚLTIMAS 3 MENSAGENS PARA LEMBRAR DO CONTEXTO SEM TRAVAR A MEMÓRIA DO PC
    historico_chat = memoria.historico[-3:] 

    termo_busca = extrair_termo_busca(mensagem)
    
    if termo_busca:
        dados_jogo = buscar_jogo_api(termo_busca)
        if dados_jogo:
            resposta = responder_llm(mensagem, dados_jogo, contexto_recomendacao, historico_chat)
            memoria.salvar(mensagem, resposta)
            return {"texto": resposta, "fonte": "API (RAWG) + LLM"}

    resposta = responder_llm(mensagem, None, contexto_recomendacao, historico_chat)
    memoria.salvar(mensagem, resposta)
    return {"texto": resposta, "fonte": "Memória Interna (Qwen LLM)"}

def _processar_pendente(texto):
    estado = memoria.estado
    jogo_mencionado = detectar_jogo(texto)
    if jogo_mencionado:
        memoria.estado = None
        return responder(texto)

    if estado == 'curtiu_jogo':
        if eh_sim(texto):
            jogo = memoria.ultimo_jogo
            if jogo in CONVERSA_PROFUNDA: return _iniciar_conversa_profunda(jogo, texto)
            similares = JOGOS[jogo]['similares']
            sugerido = random.choice(similares)
            memoria.jogo_sugerido = sugerido
            memoria.estado = 'quer_similar'
            genero = JOGOS[jogo]['genero']
            r = f"Show! Já que curte {genero}, recomendo {sugerido.title()}! Quer saber mais sobre ele?"
        elif eh_nao(texto):
            r = _tratar_negacao(texto)
            if r: return r
            memoria.estado = 'quer_genero'
            r = "De boa! Qual gênero te interessa? Survival horror, terror psicológico, jump scare, ação ou narrativo?"
        else:
            memoria.estado = None
            return responder(texto)

    elif estado == 'conversa_profunda': return _avancar_conversa_profunda(texto)

    elif estado == 'quer_similar':
        if eh_sim(texto) and memoria.jogo_sugerido in JOGOS:
            jogo = memoria.jogo_sugerido
            info = random.choice(JOGOS[jogo]['info'])
            memoria.ultimo_jogo = jogo
            memoria.estado = 'curtiu_jogo'
            r = f"{info}\n\nCurtiu {jogo.title()}?"
        elif eh_nao(texto):
            r = _tratar_negacao(texto)
            if r: return r
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
        if eh_sim(texto): r = "Legal! Me diz qual deles você quer conhecer! 👻"; memoria.estado = None
        elif eh_nao(texto): r = "De boa! Se quiser falar sobre qualquer jogo de horror, é só mandar! 🎮"; memoria.estado = None
        else: memoria.estado = None; return responder(texto)

    elif estado == 'quer_recomendacao':
        if eh_sim(texto): memoria.estado = 'quer_genero'; r = "Qual gênero te interessa? Survival horror, terror psicológico, jump scare, ação, narrativo ou ficção científica?"
        elif eh_nao(texto): r = "Sem problemas! Fala sobre qualquer jogo de horror! 👻"; memoria.estado = None
        else: memoria.estado = None; return responder(texto)
    else:
        memoria.estado = None
        return responder(texto)

    memoria.salvar(texto, r)
    return r

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
    comentario = resp_nao if eh_nao(texto) else resp_sim
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

def _tratar_negacao(texto):
    if detectar_jogo(texto): memoria.estado = None; return responder(texto)
    genero = detectar_genero(texto)
    if genero and genero in GENEROS:
        memoria.estado = 'quer_detalhe'
        r = f"Pra {genero}, recomendo: {', '.join(GENEROS[genero])}! Quer saber sobre algum?"
        memoria.salvar(texto, r)
        return r
    return None

def obter_saudacao_inicial():
    return random.choice(["Bem-vindo ao mundo do horror! 👻🎮", "Olá, aventureiro! Pronto pra conhecer jogos assustadores?"])