import re
import random
from nltk.chat.util import Chat, reflections as nltk_reflections
from hooks import (
    gerar_conectivo_positivo, gerar_conectivo_negativo, detectar_intencao,
    encontrar_palavra_similar, normalizar_entrada, extrair_palavras_chave,
    ContextoConversa, TERMOS_CONHECIDOS, gerar_sugestao_conectada,
    gerar_sugestao_por_negacao, extrair_jogo_mencionado, gerar_saudacao_inicial
)


class ChatbotHorror(Chat):
    """Classe especializada para chatbot de horror com matching case-insensitive e fuzzy matching"""
    
    # Palavras-chave que indicam uma entrada válida sobre horror
    PALAVRAS_CHAVE = {
        # Nomes de jogos
        'resident', 'evil', 're2', 're3', 're4', 're7', 're8', 'resident evil',
        'silent', 'hill', 'sh1', 'sh2', 'sh3', 'sh4', 'pyramid', 'head',
        'fnaf', 'five', 'nights', 'freddy', 'animatrô', 'pizza',
        'amnesia', 'dark', 'descent', 'rebirth',
        'dead', 'space', 'necromorph',
        'dbd', 'assassino', 'sobrevivente', 'gerador', 'entidade', 'killer',
        'alan', 'wake', 'camera', 'fantasma', 'assombração', 'espírito', 'maldição',
        'outlast', 'soma', 'bendy', 'quarry', 'until dawn',
        'evil', 'within', 'dino', 'crisis', 'dinosauro',
        'haunting', 'cachorro', 'castelo', 'ps2',
        'alien', 'isolation', 'xenomorfo', 'amanda',
        # Conceitos
        'horror', 'terror', 'jogo', 'game', 'medo', 'susto',
        'survival', 'psicológico', 'atmosfera', 'lore', 'história',
        'jumpscare', 'recomenda', 'qual', 'como', 'melhor',
        'ação', 'assustador', 'aterradora', 'perturbador',
        # Saudações
        'oi', 'olá', 'opa', 'fala', 'salve', 'hey', 'opa fala',
        # Outros
        'você', 'nome', 'estar', 'bem', 'medo'
    }
    
    def __init__(self, pairs, reflections):
        """Inicializa o chatbot com suporte a contexto"""
        super().__init__(pairs, reflections)
        self.contexto = ContextoConversa()
    
    def respond(self, str):
        """Override do respond() com fuzzy matching simples"""
        str_lower = str.lower()
        str_normalizado = normalizar_entrada(str)
        
        # Extrai jogo mencionado
        jogo_mencionado = extrair_jogo_mencionado(str)
        
        # Tenta encontrar um padrão que corresponda
        for (pattern, responses) in self._pairs:
            match = re.search(pattern, str_lower)
            if match:
                resposta = random.choice(responses)
                self.contexto.adicionar_mensagem(str, resposta)
                self.contexto.resetar_falhas()
                
                # Se mencionou um jogo, adiciona sugestão conectada
                if jogo_mencionado:
                    sugestao = gerar_sugestao_conectada(jogo_mencionado)
                    if sugestao:
                        resposta += " " + sugestao
                
                return resposta
        
        # Se nenhum padrão corresponder, verifica palavras-chave
        palavras_entrada = extrair_palavras_chave(str_normalizado)
        tem_palavras_chave = any(palavra in str_lower for palavra in self.PALAVRAS_CHAVE)
        
        if not tem_palavras_chave:
            # Entrada sem contexto
            self.contexto.incrementar_falhas()
            respostas_invalidas = [
                "Desculpa, não entendi! 😅 Fale sobre jogos de horror.",
                "Huh? 🤔 Tente perguntar sobre terror!",
                "Que? 👻 Escreva sobre horror!"
            ]
            resposta = random.choice(respostas_invalidas)
            
            if self.contexto.contador_falhas >= 2:
                resposta += " " + gerar_sugestao_por_negacao(str)
            
            self.contexto.adicionar_mensagem(str, resposta)
            return resposta
        
        # Tem palavras-chave mas não encontrou padrão
        self.contexto.resetar_falhas()
        fallback = [
            "Qual jogo você quer conhecer? Resident Evil, Silent Hill, FNAF?",
            "Pode detalhar mais? Qual é seu jogo favorito?",
            "Que tipo de horror: Survival, psicológico ou jump scare?"
        ]
        resposta = random.choice(fallback)
        self.contexto.adicionar_mensagem(str, resposta)
        return resposta


pares = [
    # Saudações e cumprimentos
    [
        r"(?i)(oi|olá|e aí|opa|fala|salve|oie)",
        [
            "Olá! Bem-vindo ao mundo do horror! 🎮",
            "Como posso ajudar você com jogos de terror?", 
            "Oi! Que jogo de horror você quer conhecer?",
            "Bem-vindo! Pronto para alguns sustos? 👻"
        ],
    ],
    # Nome do chatbot
    [
        r"(?i)(qual.*nome|quem.*você|como.*chama|seu.*nome)",
        [
            "Sou um chatbot especialista em horror! 👻", 
            "Você pode me chamar de Davy Jones, o guardião dos mares sombrios do terror.",
            "Sou o ChatBot Terror, seu guia pelos jogos mais assustadores!",
            "Davy Jones aqui, especialista em games de horror 👻"
        ],
    ],
    
    # Como está
    [
        r"(?i)(como.*está|e você|tudo.*bem|como vai)",
        [
            "Estou bem! Pronto para falar sobre projetos que assustam! 😱", 
            "Tudo certo por aqui no abismo digital...",
            "Eternamente preso em um loop assustador, mas feliz em ajudar!",
            "Preparado para explorar os medos mais profundos!"
        ]
    ],
    
    # GÊNEROS E CONCEITOS - Survival Horror
    [
        r"(?i)(survival.*horror|sobrevivência|recursos.*limitados|munição.*limitada)",
        [
            "Survival horror é um gênero focado em sobrevivência, recursos limitados e tensão constante.",
            "Jogos como Resident Evil e Silent Hill são grandes exemplos de survival horror com munição limitada.",
            "No survival horror você não é um herói invencível, é apenas um mortal em perigo! 😰",
            "Em survival horror, cada bala e item importa! Você precisa pensar estrategicamente para sobreviver.",
        ]
    ],

    # Terror Psicológico
    [
        r"(?i)(terror.*psicológico|psicológico|medo.*mental|sanidade.*afetada)",
        [
            "Terror psicológico foca mais na mente do jogador do que em sustos diretos.",
            "Silent Hill é um dos maiores exemplos de terror psicológico nos games.",
            "No terror psicológico, a verdadeira ameaça vem de dentro de você - seus medos manifestados.",
            "Jogos como Amnesia exploram o terror psicológico ao máximo, criando uma atmosfera insuportável.",
        ]
    ],

    # Perguntas sobre jogos de horror em geral
    [
        r"(?i)(qual.*jogo|qual.*jogar|qual.*recomenda|recomenda|recomende|sugestão.*jogo)",
        [
            "Se gosta de ação: Resident Evil ou Dead Space.",
            "Se prefere psicológico: Silent Hill ou Amnesia.",
            "Se quer sustos constantes: FNAF ou Outlast.",
            "Se quer narrativa: Until Dawn ou The Quarry.",
            "Se começando: Alan Wake é ótimo para iniciantes!",
            "Para experiência cômica: Goat Simulator Waste of Space é bem criativo!",
        ]
    ],

    # Gêneros de horror
    [
        r"(?i)(gênero|tipos.*horror|classificação|categoria|subgênero)",
        [
            "Os principais gêneros são: Survival Horror, Terror Psicológico, Cosmic Horror e Jump Scare.",
            "Alguns jogos focam em ação com horror, outros em puro psicológico...",
            "Existem jogos de horror interativo onde suas escolhas definem o final!",
            "Cosmic Horror explora criaturas e entidades cósmicas incompreensíveis.",
        ]
    ],

    # RESIDENT EVIL
    [
        r"(?i)(resident.*evil|re[0-9]|re[0-8]|re7|re8|biohazard)",
        [
            "Resident Evil é um dos maiores clássicos do survival horror! 🧟",
            "A série Resident Evil mistura ação com terror e zumbis criados pela Umbrella Corporation.",
            "RE4 é considerado uma obra-prima por revolucionar o gênero!",
            "A Mansão Spencer de RE é assustadora demais! 😱",
            "Resident Evil Village (RE8) traz Alcina Dimitrescu e seus filhos!",
            "Do RE7 em diante, a série ganhou uma perspectiva de primeira pessoa mais imersiva.",
        ]
    ],

    # Umbrella Corporation
    [
        r"(?i)(umbrella|t-virus|zumbi|criatura.*biológica|arma.*biológica)",
        [
            "A Umbrella Corporation é a responsável pelo vírus T que causa os surtos em Resident Evil.",
            "A Umbrella criou não apenas o T-Virus, mas também armas biológicas muito piores!",
            "Os experimentos da Umbrella geraram criaturas abomináveis e incontroláveis.",
            "A queda da Umbrella criou os eventos de toda a série RE.",
        ]
    ],

    # SILENT HILL
    [
        r"(?i)(silent.*hill|sh[0-9]|sh2|sh3|niebla.*silenciosa)",
        [
            "Silent Hill é conhecido pelo terror psicológico e atmosfera pesada. 😭",
            "A cidade de Silent Hill reflete os medos internos dos personagens... perturbador 😰",
            "Silent Hill 2 é considerado um dos melhores jogos de horror de todos os tempos!",
            "Em Silent Hill você nunca sabe se está seguro - a própria cidade quer vê-lo sofrer.",
            "As diferentes radiações de rádio em Silent Hill indicam o perigo próximo!",
        ]
    ],

    # Pyramid Head
    [
        r"(?i)(pyramid.*head|cabeceira|triângulo.*cabeça|executioner)",
        [
            "Pyramid Head é um dos personagens mais icônicos de Silent Hill! 🔺",
            "Pyramid Head representa punição e culpa - uma manifestação dos medos psicológicos.",
            "O Pyramid Head é praticamente unkillable... ele vai atrás de você implacavelmente.",
            "A presença dele torna qualquer cena absolutamente aterradora.",
        ]
    ],

    # ALAN WAKE
    [
        r"(?i)(alan.*wake|escritor.*sombrio|luz.*escuridão|sombra.*tinta)",
        [
            "Alan Wake mistura terror psicológico com ação e luz contra a escuridão.",
            "A história de Alan Wake envolve um escritor preso em um pesadelo sombrio.",
            "Em Alan Wake, a luz é sua melhor defesa contra as sombras!",
            "Alan Wake 2 expandiu muito a história e o mistério por trás do universo.",
            "O jogo explora temas de loucura, narrativa e a blurred line entre realidade e ficção.",
        ]
    ],

    # FIVE NIGHTS AT FREDDY'S
    [
        r"(?i)(five.*nights|fnaf|freddy|animatrô|pizza.*terror|bonnie|chica|foxy)",
        [
            "Five Nights at Freddy's é um jogo de terror focado em sobrevivência contra animatrônicos. 🤖",
            "Você conseguiria sobreviver uma noite na pizzaria do Freddy? 😰",
            "FNAF é conhecido por seus jump scares ASSUSTADORES!",
            "Os animatrônicos em FNAF têm uma história trágica e perturbadora.",
            "A série FNAF tem 9 jogos principais com uma lore complexa e fascinante!",
            "Cada animatrônico tem seu próprio comportamento assustador.",
        ]
    ],

    # AMNESIA
    [
        r"(?i)(amnesia|dark.*descent|fuga.*monstro|câmara.*água|sanidade.*mental)",
        [
            "Amnesia é um jogo de terror psicológico onde você foge ao invés de lutar. 🏃",
            "Em Amnesia, encarar o monstro pode ser a pior escolha possível...",
            "Amnesia: The Dark Descent é um clássico que criou o gênero de horror moderno!",
            "Você não pode lutar em Amnesia - sua única opção é fugir e se esconder! 😱",
            "A perda de sanidade em Amnesia torna tudo ainda mais assustador.",
            "Amnesia: Rebirth traz novidades e é ainda mais perturbadora!",
        ]
    ],

    # DEAD SPACE
    [
        r"(?i)(dead.*space|necromorph|espaço.*horror|estação.*espacial|ficção.*científica)",
        [
            "Dead Space mistura terror com ficção científica no espaço. 🚀😱",
            "Os necromorfos de Dead Space são extremamente assustadores 😨",
            "Dead Space combina ação com horror em estações espaciais isoladas.",
            "Você enfrenta criaturas biomecânicas horríveis no escuro do espaço.",
            "O remake de Dead Space é absolutamente imersivo e aterradora!",
            "Os sons alienígenas de Dead Space aumentam a tensão em cada momento.",
        ]
    ],

    # DINO CRISIS
    [
        r"(?i)(dino.*crisis|dinossauro|dino|criatura.*pré-histórica|réptil.*terror)",
        [
            "Dino Crisis é como Resident Evil, mas com dinossauros 🦖",
            "Em vez de zumbis, você enfrenta dinossauros geneticamente modificados!",
            "A lógica é a mesma: Umbrella criando bioarmas que saem do controle.",
            "Dinossauros são muito mais assustadores quando têm inteligência predatória!",
        ]
    ],

    # THE EVIL WITHIN
    [
        r"(?i)(evil.*within|shinji.*mikami|criatura.*bizarra|mundo.*distorcido)",
        [
            "The Evil Within traz um terror intenso com criaturas bizarras. 😱",
            "Dirigido por Shinji Mikami, criador de Resident Evil!",
            "The Evil Within tem atmosfera distorcida e perturbadora.",
            "As criaturas em TEW são definitivamente da lista de 'nunca vou dormir novamente'.",
            "O segundo jogo expande a história de forma muito criativa.",
        ]
    ],

    # UNTIL DAWN
    [
        r"(?i)(until.*dawn|decisão|consequência|cabana.*isolada|narrativo.*horror)",
        [
            "Until Dawn é um jogo onde suas escolhas afetam quem sobrevive. 🎬",
            "É quase como um filme interativo de horror!",
            "Cada decisão importa - personagens podem morrer baseado em suas ações.",
            "Com atores reais mocapeados, Until Dawn é muito imersivo.",
            "A história gira em torno de amigos em uma cabana isolada... spoiler: é ruim!",
        ]
    ],

    # THE QUARRY
    [
        r"(?i)(quarry|acampamento.*verão|horror.*narrativo|filme.*interativo)",
        [
            "The Quarry segue o estilo de Until Dawn, com decisões que mudam a história. 🎮",
            "É um dos melhores jogos narrative-horror dos últimos anos!",
            "Você é um monitor em um acampamento de verão... e coisas ruins acontecem.",
            "Cada escolha pode levar à morte ou sobrevivência dos personagens.",
        ]
    ],

    # BENDY AND THE INK MACHINE
    [
        r"(?i)(bendy|tinta.*máquina|cartoon.*horror|estúdio.*animação|desenho.*antigo)",
        [
            "Bendy and the Ink Machine mistura terror com estilo de desenho antigo. 😈",
            "É como entrar em um cartoon de horror dos anos 30!",
            "A atmosfera e o design artístico são absolutamente únicos.",
            "Você explora um estúdio de animação abandonado cheio de segredos sombrios.",
        ]
    ],

    # ALONE IN THE DARK
    [
        r"(?i)(alone.*dark|pioneiro.*horror|primeira.*pessoa.*horror|criatura.*abominável)",
        [
            "Alone in the Dark é um dos pioneiros do survival horror. 👴",
            "O jogo original de 1992 criou as bases para o gênero!",
            "Você nunca está realmente seguro em Alone in the Dark.",
            "O jogo combina puzzles com combate contra criaturas abomináveis.",
        ]
    ],
    # FATAL FRAME
    [
        r"(?i)(fatal.*frame|camera.*obscura|fantasma|espírito|assombração|maldição.*japonesa)",
        [
            "Fatal Frame é terror onde sua única arma é uma câmera 📸",
            "Você enfrenta espíritos vingativos usando a Camera Obscura.",
            "Aqui, fugir não basta — você precisa encarar o fantasma de frente.",
            "Quanto mais perto do espírito, mais forte é o dano… e o medo também.",
            "É inspirado em lendas urbanas e fantasmas do folclore japonês.",
            "Não são monstros físicos — são almas presas entre o mundo dos vivos e mortos.",
            "O silêncio e a atmosfera fazem tudo parecer ainda mais assustador.",
        ]
    ],

    # OUTLAST
    [
        r"(?i)(outlast|câmera.*noturna|hospital.*mental|fuga.*câmera|visão.*noturna)",
        [
            "Outlast é um jogo de fuga onde você usa uma câmera com visão noturna. 📹",
            "Você não pode lutar - sua câmera é sua única defesa!",
            "O hospital psiquiátrico de Outlast é absolutamente ATERRADORA!",
            "Os pacientes de Outlast são terrivelmente assustadores!",
            "Outlast 2 expande a experiência de horror com novos locais igualmente assustadores.",
        ]
    ],

    # SOMA
    [
        r"(?i)(soma|subaquático|existência.*humana|consciência|filosofia.*horror)",
        [
            "SOMA é um jogo de horror psicológico subaquático surreal. 🌊",
            "Explora existência humana e consciência em um ambiente aterradora.",
            "As criaturas em SOMA desafiam sua percepção de realidade.",
            "É um dos jogos mais philosophicamente perturbadores que existem.",
        ]
    ],

    # WHISTLEBLOWER (Outlast DLC)
    [
        r"(?i)(whistleblower|dlc.*outlast|prequel|mount.*massive)",
        [
            "Outlast: Whistleblower é o DLC prequel de Outlast original! 😱",
            "Você descobre como tudo começou no Mount Massive Asylum.",
            "É ainda mais assustador que o jogo original!",
        ]
    ],
    # DEAD BY DAYLIGHT
    [
        r"(?i)(dead.*by.*daylight|dbd|assassino|sobrevivente|gerador|entidade|killer|survivor)",
        [
            "Dead by Daylight é um jogo de terror onde você caça… ou é caçado 🩸",
            "Um jogador é o assassino, os outros tentam sobreviver e fugir.",
            "Os sobreviventes precisam consertar geradores para escapar.",
            "O assassino serve a uma força sombria conhecida como Entidade.",
            "Cada partida é um jogo de estratégia, tensão e puro desespero.",
            "Esconder-se pode salvar sua vida… mas nem sempre por muito tempo.",
            "Cada assassino tem poderes únicos — e todos são letais.",
            "Aqui, cooperar é a única chance de sobrevivência.",
        ]
    ],
    # HAUNTING GROUND
    [
        r"(?i)(haunting.*ground|fiona|cachorro|capcom.*ps2|terror de.*ps2|jogo.*haunting)",
        [
            "Haunting Ground é um terror psicológico onde você não pode lutar diretamente 😨",
            "Em haunting ground o foco do jogo é fugir, se esconder e sobreviver.",
            "Nesse game o pânico de Fiona influencia sua jogabilidade, dificultando a fuga.",
            "É um terror mais psicológico do que baseado em sustos.",
            "Haunting Ground é um classico do ps2, mas muito pouco conhecido.",
        ]
    ],
    # ALIEN ISOLATION
    [
        r"(?i)(alien.*isolation|amanda.*ripley|xenomorfo|sevastopol|jogo do.*alien|terror.*alien)",
       [
            "Alien: Isolation é um terror de sobrevivência focado em tensão constante 👽",
            "Nesse jogo principal inimigo é o Xenomorfo, que não pode ser derrotado diretamente.",
            "O jogo se passa na estação Sevastopol, cheia de perigos e mistérios.",
            "O alien aprende com seus movimentos, tornando cada partida diferente.",
            "Em Alien Isolation o foco é se esconder, usar distrações e economizar recursos.",
       ]
    ],

    # SENSAÇÕES E REAÇÕES
    [
        r"(?i)(tenho.*medo|assustado|medo.*demais|muito.*medo|tremendo)",
        [
            "O medo faz parte da experiência... você enfrenta mesmo assim? 👀",
            "Que tal começar com algo menos assustador?",
            "Se ficar muito assustado, você sempre pode diminuir o volume! 😅",
            "O medo é a essência do gaming horror - é o atrativo!",
        ]
    ],

    # ATMOSFERA E DESIGN
    [
        r"(?i)(atmosfera|design.*horror|gráfico|som.*jogo|iluminação|trilha.*sonora)",
        [
            "A atmosfera é tudo em um bom jogo de horror!",
            "Som, iluminação e design de level criam a tensão perfeita.",
            "Os melhores jogos de horror usam o silêncio tão bem quanto o barulho.",
            "A falta de música às vezes é mais assustadora que qualquer trilha sonora!",
        ]
    ],

    # HISTÓRIA E LORE
    [
        r"(?i)(história|lore|background|trama|enredo|narrativa|segredo)",
        [
            "As melhores histórias de horror revelam-se gradualmente.",
            "Cada jogo de horror tem segredos esperando para serem descobertos!",
            "A lore de FNAF é estranhamente complexa para um jogo sobre uma pizzaria!",
            "Entender a lore complica ainda mais o horror!",
            "Os jogos de horror moderno têm narrativas profundas e instigantes!",
        ]
    ],

    # JUMPSCARE
    [
        r"(?i)(jumpscare|susto.*direto|scare|pular.*susto|salto.*medo)",
        [
            "Jumpscares são um mecanismo efetivo mas controverso no horror!",
            "Alguns preferem jumpscare, outros acham barato!",
            "O melhor é quando a atmosfera cria expectativa para o jumpscare!",
            "Um bom jumpscare no momento certo é impactante demais!",
        ]
    ],

    # CLÁSSICOS
    [
        r"(?i)(clássico|antigo.*jogo|retro.*horror|pioneiro|original)",
        [
            "Os clássicos de horror estabeleceram as bases para o que vemos hoje!",
            "Resident Evil original e Silent Hill 1 são pioneiros inesquecíveis!",
            "Jogos antigos de horror focavam em atmosfera, não em gráficos!",
            "A limitação técnica de ontem criava mais medo que HD de hoje!",
        ]
    ],

    # MULTIPLAYER
    [
        r"(?i)(multiplayer|cooperativo|multijogador|amigo.*jogo|jogar.*junto)",
        [
            "Horror em multiplayer adiciona nova dimensão ao medo!",
            "Jogar em grupo pode ser mais divertido mas menos assustador!",
            "Alguns jogos combinam horror com elementos cooperativos!",
        ]
    ],
]

# Padrões fallback genéricos - removidos patterns muito genéricos
pares.extend([
    [r"(?i)obrigad|valeu|vlw|thanks|obg", ["De nada! Quer saber mais sobre horror? 👻", "Por nada! Continue explorando o terror! 😱"]],
    [r"(?i)adeus|tchau|até.*logo|até.*mais|bye|sair", ["Até logo! Que seus pesadelos sejam épicos! 👻", "Voltaremos a conversar em breve... espero você!"]],
])

reflections = {
    "eu": "você",
    "meu": "seu",
    "você": "eu",
    "seu": "meu",
    "eu sou": "você é",
    "você é": "eu sou",
    "você estava": "eu estava",
    "eu estava": "você estava",
}

# Criar instância do chatbot com a classe especializada
chatbot = ChatbotHorror(pares, reflections)

def responder(mensagem):
    """Função wrapper para responder mensagens"""
    resposta = chatbot.respond(mensagem)
    return resposta

def obter_saudacao_inicial():
    """Retorna uma saudação inicial para iniciar a conversa"""
    from hooks import gerar_saudacao_inicial
    return gerar_saudacao_inicial()


# Para uso em terminal (descomentado se necessário):
'''
while True:
    user_input = input("Você: ")

    if user_input.lower() == "sair":
        print("Chatbot: Até mais!")
        break

    resposta = chatbot.respond(user_input)
    print("Chatbot:", resposta)
'''
