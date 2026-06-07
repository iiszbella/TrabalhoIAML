from transformers import AutoTokenizer, AutoModelForCausalLM
from rawg_service import buscar_jogo_api


MODEL_PATH = "./Qwen2.5-1.5B-Instruct"

print("Carregando LLM...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    low_cpu_mem_usage=True
)

model.eval()

print("LLM carregada!")


def responder_llm(pergunta, dados_jogo=None):

    if dados_jogo:
#Controla a personalidade e da comandos para chatbot
        messages = [
            {
                "role": "system",
                "content": """
Você é um especialista em jogos de terror.
Use APENAS os dados fornecidos pela API.
Não invente informações.
Responda de forma natural e amigável.
Responda normalmente perguntas não relacionadas a jogos de terror
"""
            },
            {
                "role": "user",
                "content": f"""
Pergunta: {pergunta}

Dados oficiais:

Nome: {dados_jogo['nome']}
Nota: {dados_jogo['nota']}
Metacritic: {dados_jogo['metacritic']}
Lançamento: {dados_jogo['lancamento']}
Plataformas: {', '.join(dados_jogo['plataformas'])}
"""
            }
        ]

    else:

        messages = [
            {
                "role": "system",
                "content": """
Você é um especialista em jogos de terror.
Converse de forma amigável e natural.
"""
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.2,
        do_sample=False
    )

    input_len = inputs["input_ids"].shape[1]

    resposta = tokenizer.decode(
        outputs[0][input_len:],
        skip_special_tokens=True
    )

    return resposta.strip()