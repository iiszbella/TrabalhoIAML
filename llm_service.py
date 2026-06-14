from transformers import AutoTokenizer, AutoModelForCausalLM
from rawg_service import buscar_jogo_api
import os

# Use absolute path and prefer local files to avoid HF repo validation
MODEL_DIR = os.path.abspath("Qwen2.5-3B-Instruct")
HF_REPO = "Qwen/Qwen2.5-3B-Instruct"

print("Carregando LLM...")

try:
    # Tenta carregar modelo a partir de uma pasta local primeiro
    if os.path.isdir(MODEL_DIR):
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_DIR,
            low_cpu_mem_usage=True,
            local_files_only=True
        )
        model.eval()
        print("LLM carregada a partir de pasta local!")
    else:
        # Caso não exista pasta local, tenta carregar do Hugging Face Hub
        print(f"Pasta local não encontrada; tentando carregar do HF Hub: {HF_REPO}")
        tokenizer = AutoTokenizer.from_pretrained(HF_REPO)
        model = AutoModelForCausalLM.from_pretrained(HF_REPO, low_cpu_mem_usage=True)
        model.eval()
        print("LLM carregada a partir do Hugging Face Hub (cache/local)!")
except Exception as e:
    print("Erro ao carregar LLM:", e)
    raise


def responder_llm(pergunta, dados_jogo=None):

    if dados_jogo:
        # Controla a personalidade e dá comandos combinados (API + Conhecimento Interno)
        messages = [
            {
                "role": "system",
                "content": """
Você é um especialista em jogos de terror.
Abaixo estão os dados oficiais do jogo obtidos por uma API (nota, lançamento, plataformas).
Sua tarefa é priorizar esses dados da API na sua resposta. Porém, caso o usuário pergunte sobre elementos que NÃO estão na API (como história, personagens, dicas de gameplay ou estilo do jogo), você DEVE utilizar o seu próprio conhecimento interno para complementar a resposta de forma natural e amigável.
Responda normalmente perguntas não relacionadas a jogos de terror.
"""
            },
            {
                "role": "user",
                "content": f"""
Pergunta do Usuário: {pergunta}

Dados oficiais da API:
Nome: {dados_jogo['nome']}
Nota/Avaliação: {dados_jogo['nota']}
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