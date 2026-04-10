"""Chatbot de jogos de horror com NLTK, memória de conversa e fluxo reativo."""

import random
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
from hooks import JOGOS, GENEROS, NOMES_ALT, SIM, NAO, CONVERSA_PROFUNDA

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
        self.estado = None          # estado pendente da máquina de conversa
        self.ultimo_jogo = None     # último jogo discutido
        self.jogo_sugerido = None   # último jogo sugerido como recomendação
        self.pergunta_idx = 0       # índice da pergunta profunda atual
        self.historico = []         # histórico completo de mensagens

    def salvar(self, user, bot):
        self.historico.append({'user': user, 'bot': bot})


memoria = Memoria()

# ================================================================
# RESPONDER — FUNÇÃO PRINCIPAL
# ================================================================

def responder(mensagem):
    """Processa a mensagem do usuário e retorna uma resposta."""
    texto = mensagem.strip()
    if not texto:
        return "Não entendi! Fale sobre jogos de horror. 👻"

    # Se há uma pergunta pendente (sim/não, gênero, etc.), trata primeiro
    if memoria.estado:
        return _processar_pendente(texto)

    # Detecta jogo específico (ANTES de saudação, pois "fala sobre RE" tem "fala")
    jogo = detectar_jogo(texto)
    if jogo:
        info = random.choice(JOGOS[jogo]['info'])
        memoria.ultimo_jogo = jogo
        memoria.estado = 'curtiu_jogo'
        r = f"{info}\n\nVocê curte {jogo.title()}?"
        memoria.salvar(texto, r)
        return r

    # Saudação
    if _eh_saudacao(texto):
        r = random.choice([
            "E aí! Bora falar de jogos de horror? 🎮 Qual seu favorito?",
            "Opa! Curte jogos de terror? Me conta qual você gosta!",
            "Salve! Me diz um jogo de horror que você curte! 👻",
            "Fala! Sou o Davy Jones, seu guia no mundo do terror. Qual jogo tá na sua mente? 😱",
            "Ei! Pronto pra mergulhar no mundo do horror? Me conta um jogo que te assusta!",
            "Boa! Você veio ao lugar certo pra falar de games de terror. Por onde começamos? 🎮",
        ])
        memoria.salvar(texto, r)
        return r

    # Despedida
    if _eh_despedida(texto):
        r = random.choice([
            "Até mais! Que seus pesadelos sejam épicos! 👻",
            "Valeu! Volte quando quiser falar de terror! 🎮",
            "Até! Foi um prazer mergulhar no horror com você. 😱",
            "Flw! Se der medo sozinho, volta aqui! 👻",
            "Bye! Dorme bem... se conseguir depois de tanto papo de terror! 😈",
        ])
        memoria.salvar(texto, r)
        return r

    # Detecta gênero
    genero = detectar_genero(texto)
    if genero and genero in GENEROS:
        jogos = ', '.join(GENEROS[genero])
        memoria.estado = 'quer_detalhe'
        r = f"Pra quem curte {genero}, recomendo: {jogos}! Quer saber sobre algum deles?"
        memoria.salvar(texto, r)
        return r

    # Detecta intenção via stemming
    _, stems = tokenizar(texto)
    stems_set = set(stems)

    if _STEMS_RECOMENDACAO & stems_set:
        memoria.estado = 'quer_genero'
        r = "Qual gênero te interessa? Survival horror, terror psicológico, jump scare, ação, narrativo ou ficção científica?"
        memoria.salvar(texto, r)
        return r

    if _STEMS_IDENTIDADE & stems_set:
        memoria.estado = 'quer_recomendacao'
        r = "Sou o Davy Jones, seu guia pelos jogos mais sombrios! 👻 Quer uma recomendação?"
        memoria.salvar(texto, r)
        return r

    # "como vai" / "tudo bem"
    n = normalizar(texto)
    if any(p in n for p in ['como vai', 'tudo bem', 'como esta', 'como voce']):
        r = random.choice([
            "Tô bem! Pronto pra falar de horror! 😱 Me pergunta sobre algum jogo!",
            "De boa por aqui no abismo digital... qual jogo de terror te interessa?",
        ])
        memoria.salvar(texto, r)
        return r

    # Fallback
    r = random.choice([
        "Hmm, não captei! 🤔 Me fala um jogo de horror ou pede uma recomendação!",
        "Não entendi... tenta perguntar sobre um jogo de terror! 👻",
        "Que? 😅 Fala sobre horror! Tipo: Resident Evil, Silent Hill, FNAF...",
        "Não peguei bem... tenta citar um jogo ou pedir uma dica! 🎮",
        "Pode elaborar? Sou especialista em terror — me fala um jogo ou um estilo! 😱",
        "Não entendi, mas não desisto! Fala um jogo de horror que eu te conto tudo. 👻",
        "Hmm... será que você mencionou algo que ainda não conheço? Tenta outro jogo! 🤔",
    ])
    memoria.salvar(texto, r)
    return r


# ================================================================
# MÁQUINA DE ESTADOS — PROCESSA PERGUNTAS PENDENTES
# ================================================================

def _processar_pendente(texto):
    """Processa respostas quando há uma pergunta pendente (sim/não, gênero, etc.)."""
    estado = memoria.estado

    # REGRA PRINCIPAL: se o usuário mencionou um jogo específico,
    # respeitar isso independente do estado atual
    jogo_mencionado = detectar_jogo(texto)
    if jogo_mencionado:
        memoria.estado = None
        return responder(texto)

    if estado == 'curtiu_jogo':
        if eh_sim(texto):
            jogo = memoria.ultimo_jogo
            # Se o jogo tem conversa profunda, entra nela
            if jogo in CONVERSA_PROFUNDA:
                return _iniciar_conversa_profunda(jogo, texto)
            # Senão, sugere um similar
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
# CONVERSA PROFUNDA — perguntas interativas por jogo
# ================================================================

def _iniciar_conversa_profunda(jogo, texto):
    """Inicia a conversa profunda sobre um jogo."""
    memoria.ultimo_jogo = jogo
    memoria.pergunta_idx = 0
    memoria.estado = 'conversa_profunda'
    pergunta, _, _ = CONVERSA_PROFUNDA[jogo][0]
    r = f"Massa que curte {jogo.title()}! Bora conversar sobre ele! 🎮\n\n{pergunta}"
    memoria.salvar(texto, r)
    return r


def _avancar_conversa_profunda(texto):
    """Processa resposta na conversa profunda e avança para próxima pergunta."""
    # Se quer trocar de assunto, sai da conversa profunda
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

    # Pega a resposta adequada (sim/não) para a pergunta atual
    _, resp_sim, resp_nao = perguntas[idx]
    if eh_nao(texto):
        comentario = resp_nao
    else:
        comentario = resp_sim

    # Avança para a próxima pergunta
    memoria.pergunta_idx = idx + 1

    if memoria.pergunta_idx < len(perguntas):
        proxima, _, _ = perguntas[memoria.pergunta_idx]
        r = f"{comentario}\n\n{proxima}"
    else:
        # Acabaram as perguntas, sugere jogo similar
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
    """Quando o user diz 'não', checa se mencionou jogo ou gênero junto."""
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


# ================================================================
# SAUDAÇÃO INICIAL
# ================================================================

def obter_saudacao_inicial():
    return random.choice([
        "Bem-vindo ao mundo do horror! 👻🎮",
        "Olá, aventureiro! Pronto pra conhecer jogos assustadores?",
        "E aí! Eu sou o Davy Jones, seu guia nos games de horror. 😱",
        "Prepare-se para o terror... sou o Davy Jones e sei tudo sobre jogos de horror! 👻",
        "Olá! Entraste nas profundezas do horror digital. Vamos explorar juntos? 🎮",
        "Bem-vindo, corajoso! Aqui a gente fala só de jogos que tiram o sono. 😈",
    ])
