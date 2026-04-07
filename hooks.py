"""
hooks.py - Sistema de conectivos, saudações e tratamento de palavras para o chatbot
Gerencia fluxo de conversação após respostas positivas/negativas e fuzzy matching
"""

from difflib import SequenceMatcher
import re

# ================================================================
# SAUDAÇÕES INICIAIS
# ================================================================
SAUDACOES_INICIAIS = [
    "Bem-vindo ao mundo do horror! 👻🎮",
    "Olá, aventureiro do terror! Pronto para conhecer os jogos mais assustadores?",
    "Bem-vindo! Eu sou seu guia nos universos sombrios dos games de horror.",
    "Oi! Que jogo de horror você gostaria de explorar comigo? 😱",
    "Bem-vindo, bem-vindo... que tipo de horror o interessa?",
]

# ================================================================
# CONECTIVOS PÓS-RESPOSTA POSITIVA
# Usados para continuar a conversa quando o usuário está satisfeito
# ================================================================
CONECTIVOS_POSITIVOS = [
    "Quer saber mais sobre outro jogo?",
    "Há mais coisas interessantes que posso te contar... quer ouvir?",
    "Ficou curioso? Tenho mais horror para você! 👻",
    "Gostou? Posso falar sobre outros clássicos do terror!",
    "Que tal explorarmos outro jogo assustador?",
    "Fascinado? Deixa eu te contar sobre mais um...",
    "E se eu te dissesse que existe algo ainda mais assustador?",
    "Quer mais? Tenho uma lista inteira de pesadelos para você!",
    "Impressionado? Espere só até você saber sobre...",
    "Que bom que gostou... mas o melhor ainda está por vir! 😈",
]

# ================================================================
# CONECTIVOS PÓS-RESPOSTA NEGATIVA
# Usados para continuar a conversa quando o usuário não entendeu ou recusou
# ================================================================
CONECTIVOS_NEGATIVOS = [
    "Desculpa, deixa eu tentar de novo... qual jogo de horror você gostaria de conhecer?",
    "Hm, acho que não me expressei bem. Quer tentar de novo?",
    "Talvez eu não tenha entendido... pode reformular a pergunta?",
    "Não se preocupe! Qual aspecto do horror mais te interessa?",
    "Deixa eu ser mais claro... qual é seu tipo de terror favorito?",
    "Sem problemas! Quer explorar outro gênero de horror?",
    "Talvez você queira saber sobre um jogo específico? Qual?",
    "Entendo... vamos recomeçar. Qual jogo de horror você conhece?",
    "Desculpa pela confusão! Fale-me qual é o seu jogo favorito do gênero.",
    "Não captei direito... qual horror te chama mais atenção?",
]

# ================================================================
# VALIDAÇÃO DE ENTRADA - Fuzzy Matching
# ================================================================

def calcular_similaridade(str1, str2):
    """
    Calcula a similaridade entre duas strings usando SequenceMatcher
    Retorna um valor entre 0 e 1 (1 = idêntico)
    """
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def encontrar_palavra_similar(palavra_entrada, lista_palavras, limiar_minimo=0.75):
    """
    Encontra a palavra mais similar na lista de acordo com o limiar mínimo
    
    Args:
        palavra_entrada: A palavra que o usuário digitou
        lista_palavras: Lista de palavras válidas para comparar
        limiar_minimo: Valor mínimo de similaridade (0-1)
    
    Returns:
        Tupla (palavra_encontrada, score) ou (None, 0) se não encontrar
    """
    melhor_match = None
    melhor_score = 0
    
    for palavra in lista_palavras:
        score = calcular_similaridade(palavra_entrada, palavra)
        if score > melhor_score:
            melhor_score = score
            melhor_match = palavra
    
    if melhor_score >= limiar_minimo:
        return melhor_match, melhor_score
    return None, 0


def normalizar_entrada(texto):
    """
    Normaliza texto removendo acentos, espaços extras e convertendo para lowercase
    """
    import unicodedata
    
    # Remove acentos
    nfkd = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Remove espaços múltiplos e converte para minúsculas
    return ' '.join(texto_sem_acento.lower().split())


def extrair_palavras_chave(texto):
    """
    Extrai palavras-chave do texto removendo stopwords comuns
    """
    stopwords = {
        'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
        'de', 'da', 'do', 'das', 'dos', 'e', 'ou', 'para', 'por',
        'com', 'sem', 'em', 'no', 'na', 'nos', 'nas', 'é', 'são',
        'esse', 'essa', 'esses', 'essas', 'este', 'essa', 'estes', 'estas',
        'qual', 'quais', 'quanto', 'quantos', 'como', 'onde', 'quando',
        'me', 'te', 'se', 'nos', 'vos', 'lhe', 'lhes', 'meu', 'teu', 'seu'
    }
    
    palavras = texto.lower().split()
    return [p for p in palavras if p not in stopwords and len(p) > 2]


def sugerir_resposta_baseada_em_similaridade(entrada, palavras_validas, respostas_map):
    """
    Tenta encontrar uma resposta válida baseada em fuzzy matching
    
    Args:
        entrada: Texto do usuário
        palavras_validas: Lista de palavras/termos conhecidos
        respostas_map: Dicionário {palavra: resposta}
    
    Returns:
        Resposta encontrada ou None
    """
    entrada_normalizada = normalizar_entrada(entrada)
    palavras_entrada = extrair_palavras_chave(entrada_normalizada)
    
    melhores_matches = []
    
    for palavra in palavras_entrada:
        match, score = encontrar_palavra_similar(palavra, palavras_validas, limiar_minimo=0.7)
        if match:
            melhores_matches.append((match, score))
    
    if melhores_matches:
        # Ordena pelos mais similares
        melhores_matches.sort(key=lambda x: x[1], reverse=True)
        palavra_top = melhores_matches[0][0]
        
        if palavra_top in respostas_map:
            return respostas_map[palavra_top]
    
    return None


# ================================================================
# ESTRUTURA DE CONTEXTO DE CONVERSAÇÃO
# ================================================================

class ContextoConversa:
    """
    Mantém contexto de conversação para permitir fluxo mais natural
    """
    
    def __init__(self):
        self.historico = []
        self.ultima_resposta = None
        self.contador_falhas = 0
        self.ultimo_jogo = None
    
    def adicionar_mensagem(self, usuario_msg, bot_resposta):
        """Adiciona uma mensagem ao histórico"""
        self.historico.append({
            'usuario': usuario_msg,
            'bot': bot_resposta
        })
        self.ultima_resposta = bot_resposta
    
    def incrementar_falhas(self):
        """Incrementa contador de falhas de compreensão"""
        self.contador_falhas += 1
    
    def resetar_falhas(self):
        """Reseta contador de falhas"""
        self.contador_falhas = 0
    
    def limpar(self):
        """Limpa o contexto"""
        self.__init__()


# ================================================================
# MAPEAMENTO DE TERMOS COM FUZZY MATCHING
# ================================================================

# Dicionário de termos conhecidos para fuzzy matching
TERMOS_CONHECIDOS = {
    # Sentimentos positivos
    'gostei': ['gostei', 'adorei', 'amei', 'legal', 'awesom', 'fantastico', 'otimo', 'excelente'],
    'interessante': ['interess', 'curioso', 'intriga', 'fascinante', 'nessa'],
    'aprender': ['aprendo', 'saber', 'conhecer', 'descobrir', 'entender'],
    
    # Sentimentos negativos
    'nao_entendi': ['nao entendo', 'confuso', 'complicado', 'estranho', 'doido', 'huh', 'que'],
    'assustado': ['medo', 'medo demais', 'tremendo', 'assustado', 'aterrado', 'apavorado'],
    'entediado': ['entedi', 'chato', 'boring', 'monoton'],
    
    # Ações
    'jogar': ['jogar', 'joguei', 'joguemos', 'jogo', 'playing', 'play'],
    'recomenda': ['recomenda', 'recomende', 'sugere', 'qual jogo', 'qual game'],
    
    # Tópicos
    'historia': ['historia', 'lore', 'trama', 'enredo', 'background', 'narrativa'],
    'graficos': ['grafico', 'visual', 'arte', 'design', 'imagem', 'qualidad'],
    'som': ['som', 'sonor', 'audio', 'musica', 'trilha', 'efeito'],
}

# ================================================================
# CONECTIVOS PARA DIFERENTES CONTEXTOS
# ================================================================

CONECTIVOS_POR_CONTEXTO = {
    'positive_after_info': CONECTIVOS_POSITIVOS,
    'negative_after_info': CONECTIVOS_NEGATIVOS,
    'restart': [
        "Vamos recomeçar! Qual é seu jogo de horror favorito?",
        "Sem problemas, vamos do zero. Que tipo de horror você gosta?",
        "Deixa eu fazer uma pergunta mais simples: você prefere survival horror ou psicológico?",
    ],
    'escalate_help': [
        "Que tal você me contar qual é o seu jogo de horror favorito? Assim consigo ajudar melhor!",
        "Deixa eu te fazer uma pergunta diferente: qual foi o último jogo de horror que você jogou?",
        "Talvez seja mais fácil se você me disser um jogo de horror que você conhece.",
    ]
}

# ================================================================
# FUNCTIONS UTILITÁRIAS
# ================================================================

def gerar_saudacao_inicial():
    """Retorna uma saudação inicial aleatória"""
    import random
    return random.choice(SAUDACOES_INICIAIS)


def gerar_conectivo_positivo():
    """Retorna um conectivo positivo aleatório"""
    import random
    return random.choice(CONECTIVOS_POSITIVOS)


def gerar_conectivo_negativo():
    """Retorna um conectivo negativo aleatório"""
    import random
    return random.choice(CONECTIVOS_NEGATIVOS)


def detectar_intencao(texto):
    """
    Detecta a intenção do usuário baseado em palavras-chave
    Retorna: 'positiv', 'negativ', 'pergunta', 'info' ou 'desconhecido'
    """
    texto_lower = texto.lower()
    
    # Palavras que indicam satisfação positiva
    if any(palavra in texto_lower for palavra in ['gostei', 'adorei', 'amei', 'legal', 'bacana', 'maneiro']):
        return 'positivo'
    
    # Palavras que indicam insatisfação
    if any(palavra in texto_lower for palavra in ['nao', 'ruim', 'chato', 'entediante', 'confuso', 'nao entendo']):
        return 'negativo'
    
    # Palavras que indicam pergunta
    if any(palavra in texto_lower for palavra in ['qual', 'quando', 'onde', 'como', 'por que', 'quem', 'você']):
        return 'pergunta'
    
    # Palavras que indicam que quer mais informações
    if any(palavra in texto_lower for palavra in ['mais', 'continue', 'e tal', 'e os outros', 'mais algum']):
        return 'info'
    
    return 'desconhecido'


# ================================================================
# SISTEMA DE CONEXÕES ENTRE JOGOS E GÊNEROS
# ================================================================

# Mapeia jogos para outros jogos similares (para sugestões relacionadas)
CONEXOES_JOGOS = {
    'resident evil': {
        'similares': ['dead space', 'dino crisis', 'evil within'],
        'genero': 'survival horror',
        'descricao': 'um jogo de survival horror com zumbis e criaturas bizarras',
    },
    'silent hill': {
        'similares': ['alan wake', 'amnesia', 'soma'],
        'genero': 'terror psicológico',
        'descricao': 'um jogo de terror psicológico com atmosfera assustadora',
    },
    'fnaf': {
        'similares': ['outlast', 'alien isolation', 'five nights at freddy'],
        'genero': 'jump scare/survival',
        'descricao': 'um jogo focado em sustos constantes e tensão extrema',
    },
    'amnesia': {
        'similares': ['soma', 'outlast', 'penumbra'],
        'genero': 'terror psicológico',
        'descricao': 'um jogo de fuga onde você não pode lutar, apenas sobreviver',
    },
    'alan wake': {
        'similares': ['silent hill', 'resident evil', 'evil within'],
        'genero': 'ação + terror psicológico',
        'descricao': 'um jogo que mistura ação com narrativa de horror',
    },
    'dead space': {
        'similares': ['resident evil', 'alien isolation', 'dino crisis'],
        'genero': 'survival horror + ficção científica',
        'descricao': 'um jogo de horror no espaço com criaturas biomecânicas',
    },
    'outlast': {
        'similares': ['amnesia', 'alien isolation', 'soma'],
        'genero': 'fuga/survival',
        'descricao': 'um jogo de fuga intense em um hospital psiquiátrico',
    },
    'dino crisis': {
        'similares': ['resident evil', 'dead space', 'evil within'],
        'genero': 'survival horror',
        'descricao': 'um jogo de survival horror com dinossauros geneticamente modificados',
    },
    'alien isolation': {
        'similares': ['dead space', 'outlast', 'soma'],
        'genero': 'survival horror + ficção científica',
        'descricao': 'um jogo de tensão extrema enfrentando um xenomorfo implacável',
    },
    'until dawn': {
        'similares': ['the quarry', 'bendy', 'horrified'],
        'genero': 'narrativo interativo',
        'descricao': 'um jogo onde suas escolhas determinam quem sobrevive',
    },
}

# Mapeia gêneros para sugestões de jogos
SUGESTOES_POR_GENERO = {
    'survival horror': ['Resident Evil', 'Silent Hill', 'Dead Space', 'Evil Within'],
    'terror psicológico': ['Amnesia', 'Alan Wake', 'SOMA', 'Silent Hill'],
    'jump scare': ['Five Nights at Freddy\'s', 'Outlast', 'Bendy and the Ink Machine'],
    'ação': ['Resident Evil', 'Dead Space', 'Dino Crisis'],
    'ficção científica': ['Dead Space', 'Alien: Isolation', 'SOMA'],
    'narrativo interativo': ['Until Dawn', 'The Quarry'],
}

# Conexões baseadas em títulos parciais
MAPEAMENTO_CONEXOES = {
    'resident': 'resident evil',
    'silent': 'silent hill',
    'fnaf': 'fnaf',
    'five nights': 'fnaf',
    'amnesia': 'amnesia',
    'alan': 'alan wake',
    'dead': 'dead space',
    'outlast': 'outlast',
    'dino': 'dino crisis',
    'alien': 'alien isolation',
    'until': 'until dawn',
}


def encontrar_conexao_jogo(titulo_jogo):
    """
    Encontra a conexão de um jogo baseado no título
    Retorna um dicionário com o jogo e seus similares
    """
    titulo_norm = normalizar_entrada(titulo_jogo)
    
    # Tenta encontro exato
    if titulo_norm in CONEXOES_JOGOS:
        return CONEXOES_JOGOS[titulo_norm]
    
    # Tenta encontrar por palavra-chave
    for palavra_chave, jogo in MAPEAMENTO_CONEXOES.items():
        if palavra_chave in titulo_norm:
            if jogo in CONEXOES_JOGOS:
                return CONEXOES_JOGOS[jogo]
    
    return None


def gerar_sugestao_conectada(jogo_mencionado):
    """
    Gera uma sugestão de jogo relacionado ao jogo mencionado
    Adiciona uma pergunta se o usuário quer saber mais
    """
    import random
    
    conexao = encontrar_conexao_jogo(jogo_mencionado)
    
    if not conexao:
        return None
    
    similares = conexao.get('similares', [])
    genero = conexao.get('genero', 'horror')
    
    if not similares:
        return None
    
    jogo_sugerido = random.choice(similares)
    
    # Frases simples de conexão 
    frases = [
        f"Nesse mesmo estilo de {genero}, recomendo {jogo_sugerido}. Quer saber mais? 👻",
        f"Se você gosta de {genero}, também vai amar {jogo_sugerido}! Deseja conhecer mais?",
        f"Já que gosta desse tipo de {genero}, talvez curta {jogo_sugerido}. Quer detalhes?",
    ]
    
    return random.choice(frases)


def gerar_sugestao_por_negacao(texto_negacao):
    """
    Quando o usuário não entende ou recusa, oferece uma alternativa baseada no seu interesse
    """
    import random
    
    # Detecta que tipo de jogo o usuário pode querer
    if any(p in texto_negacao.lower() for p in ['ação', 'combate', 'lutar']):
        genero = 'ação'
        jogos = ['Resident Evil 4', 'Dead Space', 'Devil May Cry']
    elif any(p in texto_negacao.lower() for p in ['medo', 'susto', 'jumpscare']):
        genero = 'jump scare'
        jogos = ['Five Nights at Freddy\'s', 'Outlast', 'Bendy']
    elif any(p in texto_negacao.lower() for p in ['psicológico', 'mente', 'chefe']):
        genero = 'terror psicológico'
        jogos = ['Silent Hill', 'Amnesia', 'Alan Wake']
    elif any(p in texto_negacao.lower() for p in ['sobreviv', 'fugir', 'escape']):
        genero = 'survival'
        jogos = ['Outlast', 'Amnesia', 'Dead Space']
    else:
        # Padrão genérico
        genero = 'horror'
        jogos = ['Resident Evil', 'Silent Hill', 'Alan Wake']
    
    frases = [
        f"Entendo! Que tal algo mais focado em {genero}? Por exemplo: {random.choice(jogos)}?",
        f"Talvez você prefira algo com mais {genero}. Recomendo: {random.choice(jogos)}.",
        f"Sem problema! Se você busca {genero}, eu sugiro: {random.choice(jogos)}!",
    ]
    
    return random.choice(frases)


def extrair_jogo_mencionado(texto):
    """
    Extrai o nome do jogo mencionado no texto do usuário
    """
    texto_lower = normalizar_entrada(texto)
    
    for jogo in CONEXOES_JOGOS.keys():
        if jogo in texto_lower:
            return jogo
    
    for palavra_chave, jogo in MAPEAMENTO_CONEXOES.items():
        if palavra_chave in texto_lower:
            return jogo
    
    return None


if __name__ == "__main__":
    # Testes básicos
    print("=== TESTES DO SISTEMA DE HOOKS ===\n")
    
    # Teste de saudação
    print(f"Saudação inicial: {gerar_saudacao_inicial()}\n")
    
    # Teste de conectivos
    print(f"Conectivo positivo: {gerar_conectivo_positivo()}\n")
    print(f"Conectivo negativo: {gerar_conectivo_negativo()}\n")
    
    # Teste de similaridade
    print("Teste de similaridade:")
    print(f"  'resident' vs 'residencia': {calcular_similaridade('resident', 'residencia'):.2f}")
    print(f"  'silent' vs 'silente': {calcular_similaridade('silent', 'silente'):.2f}")
    print(f"  'jogo' vs 'game': {calcular_similaridade('jogo', 'game'):.2f}\n")
    
    # Teste de normalização
    print("Teste de normalização:")
    print(f"  'Resídent Evil' -> '{normalizar_entrada('Resídent Evil')}'")
    print(f"  'SILENT   HILL' -> '{normalizar_entrada('SILENT   HILL')}'")
    print(f"  'Você gosta de horror?' -> '{normalizar_entrada('Você gosta de horror?')}'")
    
    # Teste de detecção de intenção
    print("\nTeste de detecção de intenção:")
    textos_teste = [
        "Adorei essa informação!",
        "Não gostei muito.",
        "Qual é o melhor jogo?",
        "Me conte mais sobre isso.",
    ]
    for texto in textos_teste:
        intencao = detectar_intencao(texto)
        print(f"  '{texto}' -> {intencao}")
