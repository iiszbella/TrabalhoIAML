from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

AutoTokenizer.from_pretrained(MODEL_NAME)
AutoModelForCausalLM.from_pretrained(MODEL_NAME)

print("Modelo baixado!")