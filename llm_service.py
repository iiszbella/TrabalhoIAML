from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import re

MODEL_DIR = os.path.abspath("Qwen2.5-3B-Instruct")
HF_REPO = "Qwen/Qwen2.5-3B-Instruct"

print("Carregando LLM...")

try:
    if os.path.isdir(MODEL_DIR):
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, low_cpu_mem_usage=True, local_files_only=True)
        model.eval()
        print("LLM carregada a partir de pasta local!")
    else:
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
        descricao = dados_jogo.get('descricao', 'Sem descrição disponível')
        descricao = re.sub(r'<[^>]+>', '', descricao)
        if len(descricao) > 800:
            descricao = descricao[:800].strip() + "..."

        match_exato = dados_jogo.get('match_exato', True)
        termo_buscado = dados_jogo.get('termo_buscado', 'o jogo')
        nome_api = dados_jogo.get('nome', 'o jogo da API')
        
        alerta_prompt = ""
        alerta_user = ""
        
        # O SEGREDO ESTÁ AQUI: Se o Python não achou o nome exato, nós damos uma bronca prévia na IA
        if not match_exato:
            alerta_prompt = f"""
!!! ALERTA CRÍTICO DE CONTEXTO !!!
O usuário perguntou sobre: '{termo_buscado}'
Mas a busca oficial da API retornou os dados de outro jogo: '{nome_api}'.
REGRA OBRIGATÓRIA: Você DEVE começar sua resposta explicando esse desencontro. 
NÃO diga que '{termo_buscado}' foi lançado na data abaixo. Diga que '{nome_api}' foi lançado na data abaixo.
"""
            alerta_user = f"\n\n[INSTRUÇÃO DO SISTEMA: Lembre-se, os dados abaixo são do jogo '{nome_api}' e NÃO de '{termo_buscado}'. Avise o usuário sobre essa troca feita pela busca!]"

        system_prompt = f"""Você é Davy Jones, um especialista em games.
Eu vou te fornecer um Documento de Banco de Dados Oficial retornado pela API RAWG.

REGRAS OBRIGATÓRIAS:
1. USE SOMENTE OS DADOS DA API: Para notas, datas de lançamento e plataformas.
2. TRADUÇÃO: A descrição abaixo está em inglês. Leia e explique de forma resumida em Português.
3. SEJA HONESTO: Nunca invente datas ou notas.
{alerta_prompt}
[DOCUMENTO OFICIAL DA API RAWG]
NOME DO JOGO NESTE DOCUMENTO: {nome_api}
LANÇAMENTO: {dados_jogo.get('lancamento')}
NOTA DOS JOGADORES: {dados_jogo.get('nota')}
NOTA METACRITIC: {dados_jogo.get('metacritic')}
PLATAFORMAS: {', '.join(dados_jogo.get('plataformas', []))}
DESCRIÇÃO: {descricao}
[FIM DO DOCUMENTO]"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Pergunta: {pergunta}{alerta_user}"}
        ]

    else:
        messages = [
            {"role": "system", "content": "Você é Davy Jones, um especialista em jogos. Responda de forma natural e amigável usando seu próprio conhecimento."},
            {"role": "user", "content": pergunta}
        ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        do_sample=False
    )

    input_len = inputs["input_ids"].shape[1]

    resposta = tokenizer.decode(
        outputs[0][input_len:],
        skip_special_tokens=True
    )

    return resposta.strip()