"""Banco de dados de jogos de horror e constantes do chatbot."""

JOGOS = {
    'resident evil': {
        'info': [
            'Resident Evil é um dos maiores clássicos do survival horror! Zumbis, Umbrella Corporation e muita tensão. 🧟',
            'A série RE mistura ação com terror. RE4 é considerado uma obra-prima!',
            'Do RE7 em diante, a série ganhou perspectiva em primeira pessoa, muito mais imersiva.',
        ],
        'genero': 'survival horror',
        'similares': ['dead space', 'dino crisis', 'evil within'],
        'tags': ['resident', 'biohazard', 're2', 're3', 're4', 're7', 're8', 'umbrella', 'zumbi'],
    },
    'silent hill': {
        'info': [
            'Silent Hill é referência em terror psicológico. A cidade reflete os medos dos personagens. 😰',
            'Silent Hill 2 é considerado um dos melhores jogos de horror de todos os tempos!',
            'O Pyramid Head é um dos vilões mais icônicos — representa culpa e punição.',
        ],
        'genero': 'terror psicológico',
        'similares': ['alan wake', 'amnesia', 'soma'],
        'tags': ['silent', 'hill', 'pyramid', 'head'],
    },
    'fnaf': {
        'info': [
            "Five Nights at Freddy's é focado em sobrevivência contra animatrônicos assassinos. 🤖",
            'FNAF é famoso pelos jump scares e uma lore extremamente complexa!',
            'São 9 jogos com uma história trágica por trás dos animatrônicos.',
        ],
        'genero': 'jump scare',
        'similares': ['outlast', 'bendy'],
        'tags': ['fnaf', 'freddy', 'animatronico', 'five', 'nights', 'bonnie', 'chica', 'foxy'],
    },
    'amnesia': {
        'info': [
            'Em Amnesia você não pode lutar — só fugir e se esconder! 😱',
            'Amnesia: The Dark Descent praticamente criou o gênero moderno de horror indie.',
            'A mecânica de sanidade torna o jogo ainda mais aterrorizante.',
        ],
        'genero': 'terror psicológico',
        'similares': ['soma', 'outlast', 'silent hill'],
        'tags': ['amnesia', 'descent', 'rebirth', 'sanidade'],
    },
    'alan wake': {
        'info': [
            'Alan Wake mistura terror psicológico com ação — luz contra a escuridão. 🔦',
            'A história envolve um escritor preso em um pesadelo sombrio e criativo.',
            'Alan Wake 2 expandiu o mistério de forma brilhante.',
        ],
        'genero': 'terror psicológico',
        'similares': ['silent hill', 'evil within', 'resident evil'],
        'tags': ['alan', 'wake', 'escritor'],
    },
    'dead space': {
        'info': [
            'Dead Space mistura terror com ficção científica no espaço. 🚀😱',
            'Os necromorfos são criaturas biomecânicas absolutamente horríveis.',
            'O remake trouxe uma experiência ainda mais imersiva e aterrorizante.',
        ],
        'genero': 'survival horror',
        'similares': ['resident evil', 'alien isolation', 'dino crisis'],
        'tags': ['necromorfo', 'necromorph'],
    },
    'outlast': {
        'info': [
            'Outlast é um jogo de fuga com câmera de visão noturna como única defesa. 📹',
            'O hospital psiquiátrico Mount Massive é absolutamente aterrorizante!',
            'Outlast 2 expande a experiência com cenários igualmente perturbadores.',
        ],
        'genero': 'survival',
        'similares': ['amnesia', 'alien isolation', 'soma'],
        'tags': ['outlast', 'hospital', 'whistleblower'],
    },
    'dino crisis': {
        'info': [
            'Dino Crisis é como Resident Evil, mas com dinossauros! 🦖',
            'Dinossauros geneticamente modificados com inteligência predatória.',
            'Um clássico subestimado que merece mais reconhecimento.',
        ],
        'genero': 'survival horror',
        'similares': ['resident evil', 'dead space'],
        'tags': ['dino', 'dinossauro'],
    },
    'evil within': {
        'info': [
            'The Evil Within traz terror intenso com criaturas bizarras. 😱',
            'Dirigido por Shinji Mikami, o criador de Resident Evil!',
            'O mundo distorcido do jogo é absolutamente perturbador.',
        ],
        'genero': 'survival horror',
        'similares': ['resident evil', 'silent hill'],
        'tags': ['within', 'shinji', 'mikami'],
    },
    'until dawn': {
        'info': [
            'Until Dawn é um jogo onde suas escolhas decidem quem vive ou morre. 🎬',
            'Quase um filme interativo de horror com atores reais.',
            'Cada decisão importa — qualquer personagem pode morrer.',
        ],
        'genero': 'narrativo',
        'similares': ['the quarry', 'bendy'],
        'tags': ['until', 'dawn'],
    },
    'the quarry': {
        'info': [
            'The Quarry segue o estilo Until Dawn — decisões que mudam tudo. 🎮',
            'Monitores num acampamento de verão... e coisas horríveis acontecem.',
            'Um dos melhores jogos de horror narrativo dos últimos anos.',
        ],
        'genero': 'narrativo',
        'similares': ['until dawn'],
        'tags': ['quarry', 'acampamento'],
    },
    'soma': {
        'info': [
            'SOMA é horror psicológico subaquático que questiona a existência humana. 🌊',
            'As criaturas desafiam sua percepção de realidade e consciência.',
            'Um dos jogos mais filosoficamente perturbadores que existem.',
        ],
        'genero': 'terror psicológico',
        'similares': ['amnesia', 'outlast'],
        'tags': ['soma', 'subaquatico', 'consciencia'],
    },
    'dead by daylight': {
        'info': [
            'Dead by Daylight: você caça... ou é caçado. 🩸',
            'Um jogador é o assassino, os outros tentam sobreviver e escapar.',
            'Cada assassino tem poderes únicos e mortais.',
        ],
        'genero': 'multiplayer',
        'similares': ['until dawn'],
        'tags': ['daylight', 'dbd', 'killer'],
    },
    'alien isolation': {
        'info': [
            'Alien: Isolation é tensão pura contra um Xenomorfo implacável. 👽',
            'O alien aprende com seus movimentos — cada partida é diferente.',
            'Esconder, distrair e economizar recursos: a chave da sobrevivência.',
        ],
        'genero': 'survival horror',
        'similares': ['dead space', 'outlast', 'soma'],
        'tags': ['alien', 'xenomorfo', 'ripley', 'sevastopol'],
    },
    'fatal frame': {
        'info': [
            'Fatal Frame: sua única arma é uma câmera contra espíritos. 📸',
            'A Camera Obscura captura fantasmas do folclore japonês.',
            'Quanto mais perto do espírito, mais dano... e mais medo.',
        ],
        'genero': 'terror psicológico',
        'similares': ['silent hill', 'haunting ground'],
        'tags': ['fatal', 'obscura'],
    },
    'haunting ground': {
        'info': [
            'Haunting Ground: terror psicológico onde você só foge e se esconde. 😨',
            'O pânico de Fiona afeta diretamente a jogabilidade.',
            'Clássico do PS2, pouco conhecido mas muito intenso.',
        ],
        'genero': 'terror psicológico',
        'similares': ['fatal frame', 'silent hill'],
        'tags': ['haunting', 'fiona'],
    },
    'bendy': {
        'info': [
            'Bendy and the Ink Machine: terror com estilo de cartoon antigo. 😈',
            'Um estúdio de animação abandonado cheio de segredos sombrios.',
            'Design artístico único que mistura nostalgia com horror.',
        ],
        'genero': 'ação + horror',
        'similares': ['fnaf', 'until dawn'],
        'tags': ['bendy', 'tinta', 'ink', 'machine', 'cartoon'],
    },
}

# Nomes alternativos para jogos (alias → chave em JOGOS)
NOMES_ALT = {
    'five nights at freddy': 'fnaf',
    'five nights': 'fnaf',
    'biohazard': 'resident evil',
    're village': 'resident evil',
}

GENEROS = {
    'survival horror': ['Resident Evil', 'Dead Space', 'Dino Crisis', 'Evil Within', 'Alien Isolation'],
    'terror psicológico': ['Silent Hill', 'Amnesia', 'SOMA', 'Alan Wake', 'Fatal Frame', 'Haunting Ground'],
    'jump scare': ['FNAF', 'Outlast', 'Bendy'],
    'ação': ['Resident Evil', 'Dead Space', 'Alan Wake', 'Evil Within'],
    'narrativo': ['Until Dawn', 'The Quarry'],
    'multiplayer': ['Dead by Daylight'],
    'ficção científica': ['Dead Space', 'Alien Isolation', 'SOMA'],
}

SIM = {'sim', 'ss', 'claro', 'certeza', 'obvio', 'demais', 'bora', 'quero',
       'show', 'massa', 'top', 'yes', 'adoro', 'gosto', 'curto', 'amo',
       'joguei', 'conheco', 'manda', 'pode', 'dale', 'vamos', 's', 'sip',
       'aham', 'uhum', 'yeah', 'siiim', 'siim', 'isso', 'ja', 'com certeza'}

NAO = {'nao', 'não', 'nope', 'nunca', 'nem', 'negativo', 'passo', 'nah',
       'n', 'nn', 'nada', 'naoo', 'nop'}

# ================================================================
# PERGUNTAS PROFUNDAS — Conversa interativa por jogo
# Cada entry: (pergunta do bot, respostas para sim, respostas para não)
# ================================================================

CONVERSA_PROFUNDA = {
    'resident evil': [
        ("Você já jogou o Resident Evil 1, o clássico que começou tudo? 🏚️",
         "A mansão Spencer é icônica! Aqueles puzzles e corredores escuros marcaram uma geração. Sabia que o jogo quase foi cancelado?",
         "Vale muito a pena! É o começo de tudo — sobreviver na mansão Spencer com recursos limitados é uma experiência única."),
        ("Curte mais o estilo clássico (câmera fixa) ou o moderno (primeira/terceira pessoa)?",
         "O estilo clássico tem um charme especial! A câmera fixa criava uma tensão absurda porque você nunca sabia o que vinha pela frente.",
         "O estilo moderno é mais imersivo mesmo! RE4 revolucionou com a câmera sobre o ombro, e RE7/RE8 em primeira pessoa são de arrepiar."),
        ("RE4 é considerado uma obra-prima. Você já jogou? 🎮",
         "RE4 mudou o gênero inteiro! A aldeia, os Ganados, o Krauser... e o modo Mercenaries é viciante demais!",
         "RE4 é obrigatório! Mistura ação com tensão perfeitamente. O remake de 2023 ficou incrível, recomendo começar por ele."),
        ("E o RE2 Remake? Muita gente considera o melhor remake já feito!",
         "O Mr. X te perseguindo pelos corredores é de gelar o sangue! A delegacia de Raccoon City nunca foi tão aterrorizante. 😱",
         "O RE2 Remake é sensacional! Te coloca na pele de Leon ou Claire na delegacia infestada de zumbis. Imperdível!"),
        ("Você conhece a história da Umbrella Corporation? 🧬",
         "A Umbrella é uma das vilãs mais icônicas dos games! O T-Virus, o G-Virus, os experimentos... cada jogo revela mais da conspiração.",
         "A Umbrella é a empresa farmacêutica que criou o T-Virus e causou o apocalipse zumbi. A trama dela conecta TODOS os jogos da série!"),
        ("RE7 mudou tudo com a primeira pessoa. Curtiu essa mudança?",
         "A família Baker é assustadora demais! Jack te perseguindo é puro terror. E a conexão com a saga principal surpreendeu todo mundo.",
         "Muita gente estranhou no começo, mas RE7 salvou a série! É muito mais imersivo e a família Baker é inesquecível. Recomendo!"),
        ("Village (RE8) com a Lady Dimitrescu... jogou? 🧛‍♀️",
         "O castelo Dimitrescu é lindo e aterrorizante ao mesmo tempo! E a parte do Beneviento... aquela casa de bonecas é perturbadora demais.",
         "RE8 mistura vários tipos de horror: vampiros, lobisomens, bonecas... a Lady Dimitrescu virou um ícone instantâneo da franquia!"),
        ("Qual vilão de RE te assusta mais? Nemesis, Mr. X, Jack Baker? 😈",
         "Boa escolha! Os stalkers de RE são únicos — cada um cria um tipo diferente de tensão. Nemesis gritando 'STARS' é traumático!",
         "Todos são assustadores de formas diferentes! Nemesis é implacável, Mr. X é silencioso e opressor, Jack Baker é insano."),
        ("Sabia que RE tem filmes, séries e até animações? Já viu algum?",
         "Os filmes são polêmicos entre os fãs, mas as animações como Degeneration e Damnation são bem fiéis ao jogo!",
         "Tem os filmes live-action da Milla Jovovich, a série da Netflix, e animações em CGI. As animações são as mais fiéis aos games!"),
        ("Se pudesse escolher UM RE pra jogar pela primeira vez de novo, qual seria?",
         "Escolha difícil! Cada um tem seu brilho. RE2 Remake pela perfeição, RE4 pela diversão, RE7 pelo terror puro... todos são memoráveis! 🎮",
         "Eu recomendaria RE2 Remake pra quem quer terror, RE4 pra quem quer ação, ou RE7 pra quem quer se borrar de medo! 😱"),
    ],
    'silent hill': [
        ("Você já jogou Silent Hill 2? É considerado o auge do terror psicológico! 😰",
         "SH2 é uma obra de arte! A história de James e Maria é devastadora. O final te faz repensar TUDO que aconteceu no jogo.",
         "SH2 é obrigatório pra quem curte terror! A história de James buscando sua esposa morta em Silent Hill é profundamente perturbadora."),
        ("O Pyramid Head te assusta? Ele é um dos vilões mais icônicos do horror! 🔺",
         "Pyramid Head é genial porque ele não é só um monstro — ele representa a culpa e o desejo de punição. Puro terror psicológico!",
         "Mesmo sem jogar, Pyramid Head é cultural! Ele aparece arrastando aquela espada gigante e simboliza os demônios internos dos personagens."),
        ("Prefere o terror psicológico de SH ou o mais ação de outros jogos?",
         "SH é mestre em mexer com sua mente! A neblina, os sons, nunca saber se o que você vê é real... é uma experiência diferente de tudo.",
         "Muita gente prefere ação, e tá tudo bem! Mas SH prova que o medo mais forte vem de dentro, não de monstros que você pode matar."),
        ("A trilha sonora do Akira Yamaoka é lendária. Já ouviu? 🎵",
         "Yamaoka é um gênio! Mistura industrial, rock e ambient de um jeito que só Silent Hill tem. 'Theme of Laura' é de chorar!",
         "Procura no YouTube! A trilha do SH é considerada uma das melhores de todos os games. Funciona até fora do jogo, é linda e assustadora."),
        ("Sabia que a cidade de Silent Hill reflete os medos de cada personagem?",
         "É o que torna SH tão especial! Cada personagem vê uma Silent Hill diferente, moldada pelos seus traumas. O mapa muda com a psique!",
         "É fascinante! A cidade é uma entidade que manifesta os medos de quem entra. Por isso os monstros de cada jogo são únicos pro personagem."),
        ("SH1 no PS1 e SH3 são muito subestimados. Conhece? 🎮",
         "SH1 é o original que criou tudo — Alessa, a seita, o fog! E SH3 continua a história com Heather de forma brilhante.",
         "SH1 começou tudo com a história de Harry buscando sua filha. SH3 traz Heather, filha de Harry, e fecha o arco de forma incrível!"),
        ("O que te assusta mais: monstros ou o silêncio de SH?",
         "O silêncio é arma poderosa em SH! Quando o rádio para de fazer estática, você SABE que algo vai acontecer... e a espera é o pior.",
         "Os dois funcionam juntos! Os monstros simbolizam traumas, e o silêncio te prepara psicologicamente pro horror. Genialidade pura."),
        ("Você joga no escuro com fone? É a forma definitiva de jogar SH! 🎧",
         "Corajoso! SH no escuro com fone é uma experiência que marca pra vida. Cada som, cada passo, cada estática do rádio fica 10x mais intenso!",
         "Se um dia tiver coragem, tenta! O design de som do SH foi feito pra fones. Muda completamente a experiência de terror."),
        ("O remake de SH2 pela Bloober Team... o que acha?",
         "Reimaginar SH2 é uma responsabilidade enorme! Os fãs tinham expectativas altíssimas. É interessante ver como uma obra-prima é reinterpretada.",
         "Independente do remake, o SH2 original sempre vai ser especial. Mas é bom ver a franquia recebendo atenção de novo!"),
        ("Se Silent Hill fosse real, você entraria na neblina? 🌫️",
         "Corajoso! Lembre-se: a cidade mostra seus piores medos. O que apareceria pra você? Esse é o verdadeiro terror de Silent Hill!",
         "Sábia decisão! 😂 Ninguém sano entraria naquela neblina. Mas é isso que torna SH tão fascinante — o horror de enfrentar a si mesmo."),
    ],
    'alan wake': [
        ("Você já jogou Alan Wake 1? A história do escritor preso no pesadelo é incrível! 🔦",
         "AW1 é genial! A mecânica de luz contra escuridão é única. E a narrativa em formato de série de TV é muito criativa!",
         "AW1 é uma experiência única! Você é um escritor cuja história de terror se torna realidade. A mecânica de usar luz como arma é brilhante."),
        ("A mecânica de usar luz pra derrotar inimigos te agrada? 🔦",
         "É uma das mecânicas mais criativas do horror! Lanterna + flare gun + holofotes criam um gameplay totalmente diferente.",
         "É bem diferente do usual! Em vez de só atirar, você precisa 'descascar' a escuridão dos inimigos com luz antes de poder derrotá-los."),
        ("Alan Wake tem uma pegada muito de Stephen King. Curte esse estilo? 📖",
         "A influência é clara! Cidade pequena, escritor, forças sobrenaturais... é como jogar um livro do King. A atmosfera de Bright Falls é perfeita!",
         "O jogo é inspirado em Stephen King e Twin Peaks! Bright Falls é uma cidadezinha americana com segredos sombrios. Clima de thriller literário!"),
        ("A série foi feita em formato de episódios de TV. Curtiu essa estrutura?",
         "Cada episódio termina com um cliffhanger e a tela 'Previously on Alan Wake'! É como maratonar uma série de terror. Super criativo!",
         "É bem diferente! Cada capítulo funciona como um episódio, com resumo do anterior e trilha sonora no final. Dá vontade de jogar mais!"),
        ("Alan Wake 2 veio depois de 13 anos. Já jogou? 😱",
         "A espera valeu! AW2 é mais sombrio, mais complexo, e a adição da agente Saga Anderson trouxe uma perspectiva nova incrível!",
         "AW2 finalmente saiu em 2023! É mais terror psicológico que o primeiro, com gráficos absurdos e narrativa dupla entre Alan e Saga."),
        ("Sabia que Alan Wake se conecta com Control, outro jogo da Remedy?",
         "O Remedy Connected Universe é fascinante! O DLC de Control 'AWE' conecta os dois jogos. A Remedy está criando seu próprio multiverso!",
         "A Remedy criou um universo compartilhado! Alan Wake e Control existem no mesmo mundo. O DLC 'AWE' de Control traz o Alan diretamente."),
        ("O que te assusta mais em AW: os Taken ou a própria escuridão? 🌑",
         "A escuridão em AW não é só ausência de luz — é uma ENTIDADE. Os Taken são pessoas consumidas por ela. O conceito é aterrorizante!",
         "Os dois funcionam juntos! A Dark Presence é uma força que consome pessoas, transformando-as em Taken. A floresta à noite é opressiva."),
        ("Bright Falls e Cauldron Lake... a ambientação te agrada?",
         "A ambientação pacífica do noroeste americano em contraste com o horror é genial! De dia tudo parece tranquilo, de noite é pesadelo!",
         "O cenário é lindo e sinistro! Floresta densa, lagos escuros, uma cidadezinha isolada... perfeito pra uma história de terror."),
        ("AW tem umas músicas épicas, como 'War' do Poets of the Fall. Ouviu? 🎵",
         "A cena do 'War' na fazenda de Barry com o palco de rock é LENDÁRIA! E 'The Poet and the Muse' do Old Gods of Asgard é parte da lore!",
         "Procura 'Alan Wake War scene' no YouTube! É uma das cenas mais icônicas de um jogo. Música e gameplay juntos de forma épica!"),
        ("Se você fosse escritor como Alan, teria coragem de usar o manuscrito? ✍️",
         "O dilema do Alan é fascinante: tudo que ele escreve se torna real, mas ele não pode controlar como! Seria tentador e aterrorizante!",
         "Sábia escolha! O manuscrito é uma bênção e maldição. Tudo que Alan escreve acontece, mas de formas distorcidas e sombrias. Melhor não arriscar! 😅"),
    ],
}
