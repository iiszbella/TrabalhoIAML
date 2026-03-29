import random
import nltk
from nltk.chat.util import Chat, reflections

pares = [
    [
        r"Oi|Olá|E aí",
        [
            "Olá!","Como posso ajudar você?", "Oi, como está?"
        ],
    ],
    [
        r"Qual é o seu nome?",
        [
            "Sou um chatbot simples.", "Você pode me chamar de Chatbot.", "Sou o ChatBot."
        ],
    ],
    [
        r"Como você está?",
        [
            "Estou bem!", "Tudo certo por aqui."
        ]
    ],
    [
        r"(.*)\?",
        [
            "Desculpe, não tenho uma resposta específica para essa pergunta.", "Pode reformular a pergunta?"
        ],
    ],
    #CONCEITOS GERAIS
    [
        r".*survival horror.*",
        [
            "Survival horror é um gênero focado em sobrevivência, recursos limitados e tensão constante.",
            "Jogos como Resident Evil e Silent Hill são grandes exemplos de survival horror.",
        ]
    ],

    [
        r".*terror psicológico.*",
        [
            "Terror psicológico foca mais na mente do jogador do que em sustos diretos.",
            "Silent Hill é um dos maiores exemplos de terror psicológico nos games.",
        ]
    ],

    [
        r".*jogo.*terror.*",
        [
            "Jogos de terror podem ser de sobrevivência, psicológico ou ação.",
            "Você prefere sustos diretos ou aquele medo que fica na cabeça? 😨"
        ]
    ],

    #RESIDENT EVIL
    [
        r".*resident evil.*",
        [
            "Resident Evil é um dos maiores clássicos do survival horror.",
            "A série Resident Evil mistura ação com terror e zumbis criados pela Umbrella Corporation.",
        ]
    ],

    [
        r".*umbrella.*",
        [
            "A Umbrella Corporation é a responsável pelo vírus que causa os surtos em Resident Evil.",
        ]
    ],

    #SILENT HILL
    [
        r".*silent hill.*",
        [
            "Silent Hill é conhecido pelo terror psicológico e atmosfera pesada.",
            "A cidade de Silent Hill reflete os medos internos dos personagens... perturbador 😰",
        ]
    ],

    [
        r".*pyramid head.*",
        [
            "Pyramid Head é um dos personagens mais icônicos de Silent Hill.",
        ]
    ],

    #ALAN WAKE
    [
        r".*alan wake.*",
        [
            "Alan Wake mistura terror psicológico com ação e luz contra a escuridão.",
            "A história de Alan Wake envolve um escritor preso em um pesadelo sombrio.",
        ]
    ],

    #FNAF
    [
        r".*five nights.*|.*fnaf.*",
        [
            "Five Nights at Freddy's é um jogo de terror focado em sobrevivência contra animatrônicos.",
            "Você conseguiria sobreviver uma noite na pizzaria do Freddy? 😰",
        ]
    ],

    #AMNESIA
    [
        r".*amnesia.*",
        [
            "Amnesia é um jogo de terror psicológico onde você foge ao invés de lutar.",
            "Em Amnesia, encarar o monstro pode ser a pior escolha possível...",
        ]
    ],

    #DEAD SPACE
    [
        r".*dead space.*",
        [
            "Dead Space mistura terror com ficção científica no espaço.",
            "Os necromorfos de Dead Space são extremamente assustadores 😨",
        ]
    ],

    #DINO CRISIS
    [
        r".*dino crisis.*",
        [
            "Dino Crisis é como Resident Evil, mas com dinossauros.",
        ]
    ],

    #THE EVIL WITHIN
    [
        r".*evil within.*",
        [
            "The Evil Within traz um terror intenso com criaturas bizarras.",
        ]
    ],

    #UNTIL DAWN
    [
        r".*until dawn.*",
        [
            "Until Dawn é um jogo onde suas escolhas afetam quem sobrevive.",
        ]
    ],

    #THE QUARRY
    [
        r".*the quarry.*",
        [
            "The Quarry segue o estilo de Until Dawn, com decisões que mudam a história.",
        ]
    ],

    #BENDY
    [
        r".*bendy.*",
        [
            "Bendy and the Ink Machine mistura terror com estilo de desenho antigo.",
        ]
    ],

    #ALONE IN THE DARK
    [
        r".*alone in the dark.*",
        [
            "Alone in the Dark é um dos pioneiros do survival horror.",
        ]
    ],

    #RECOMENDAÇÃO
    [
        r".*recomenda.*jogo.*",
        [
            "Se gosta de ação: Resident Evil.",
            "Se prefere psicológico: Silent Hill.",
            "Se quer sustos constantes: FNAF ou Outlast.",
        ]
    ],

    #MEDO
    [
        r".*tenho medo.*",
        [
            "O medo faz parte da experiência... você encara mesmo assim? 👀",
        ]
    ],
]

pares.extend([
    [r"(.+)",["Entendi. Diga-me mais.", "Pode me contar mais sobre isso?", "Interessante. Conte-me mais..."]],
    [r"(.*)\?", ["Hmm... não tenho certeza sobre isso...", "Essa é difícil..."]],
    [r"(.+)", ["Interessante... continue", "Conte mais..."]]
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

chatbot = Chat(pares, reflections)

def responder(mensagem):
    return chatbot.respond(mensagem)


#Usar o chatbot pelo terminal, sem Flask
'''
while True:
    user_input = input("Você: ")

    if user_input.lower() == "sair":
        print("Chatbot: Até mais!")
        break

    resposta = chatbot.respond(user_input)
    print("Chatbot:", resposta)
'''