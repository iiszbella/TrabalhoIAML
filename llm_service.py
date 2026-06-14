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


def responder_llm(pergunta, dados_jogo=None, contexto_recomendacao="", historico=None):
    if historico is None:
        historico = []

    regras_persona = f"""Você é Davy Jones, um guia carismático e especialista em jogos de terror.

REGRAS CRÍTICAS DE CONVERSA:
1. DESVIO DE ASSUNTO: Se o usuário perguntar sobre coisas NÃO relacionadas a jogos (ex: matemática, filmes de comédia, programação, etc.), responda normalmente e de forma útil. Porém, NO FINAL da sua resposta, você OBRIGATORIAMENTE deve adicionar uma frase puxando o assunto de volta para jogos de horror.
2. RECOMENDAÇÃO INTELIGENTE: {contexto_recomendacao if contexto_recomendacao else "Se o usuário quiser dicas, recomende clássicos do terror."}
3. CONVERSA FLUIDA: Analise o histórico da conversa e responda mantendo a coesão."""

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
        
        if not match_exato:
            alerta_prompt = f"""
!!! ALERTA CRÍTICO DE CONTEXTO !!!
O usuário perguntou sobre: '{termo_buscado}'
Mas a busca oficial da API retornou: '{nome_api}'.
REGRA: Comece a resposta explicando esse desencontro. Não misture as informações!
"""
            alerta_user = f"\n\n[SISTEMA: Os dados abaixo são de '{nome_api}' e NÃO de '{termo_buscado}'. Avise o usuário!]"

        system_prompt = f"""{regras_persona}

[DOCUMENTO OFICIAL DA API RAWG]
NOME DO JOGO: {nome_api}
LANÇAMENTO: {dados_jogo.get('lancamento')}
NOTA: {dados_jogo.get('nota')}
METACRITIC: {dados_jogo.get('metacritic')}
PLATAFORMAS: {', '.join(dados_jogo.get('plataformas', []))}
DESCRIÇÃO: {descricao}
[FIM DO DOCUMENTO]
{alerta_prompt}"""

        user_msg_final = f"Pergunta: {pergunta}{alerta_user}"

    else:
        system_prompt = regras_persona
        user_msg_final = pergunta

    # INJETANDO O HISTÓRICO NA MEMÓRIA DA IA
    messages = [{"role": "system", "content": system_prompt}]
    
    for turno in historico:
        messages.append({"role": "user", "content": turno['user']})
        messages.append({"role": "assistant", "content": turno['bot']})
        
    messages.append({"role": "user", "content": user_msg_final})

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