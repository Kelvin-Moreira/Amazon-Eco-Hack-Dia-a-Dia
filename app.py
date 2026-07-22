import os
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)
CORS(app)

# Rota para abrir a página inicial
@app.route('/')
def pagina_inicial():
    return send_file('index.html')

# Rota NOVA: Permite que o navegador leia o gemma_client.js e o config.json
@app.route('/<path:filename>')
def arquivos_estaticos(filename):
    return send_from_directory(os.getcwd(), filename)

MODEL_ID = "google/gemma-2-2b-it"

print("⏳ Carregando o modelo Gemma 2B para a memória...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    torch_dtype=torch.bfloat16
)
print("✅ Modelo carregado e pronto para inferência!")

@app.route('/api/gemma/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    system_prompt = data.get("system_prompt", "")
    messages = data.get("messages", [])
    
    # TRATAMENTO PARA O GEMMA: Converte o system_prompt em instrução na primeira mensagem, 
    # já que o Gemma-2 não suporta a role "system" separada.
    formatted_messages = []
    if system_prompt and messages:
        # Copia as mensagens para não alterar o histórico original
        messages_copy = [dict(m) for m in messages]
        # Injeta o prompt de sistema como instrução inicial na primeira fala do usuário
        messages_copy[0]["content"] = f"[Instruções de Comportamento do Sistema: {system_prompt}]\n\n{messages_copy[0]['content']}"
        formatted_messages = messages_copy
    else:
        formatted_messages = messages

    # Constrói o template apenas com roles de usuário e assistente suportadas
    prompt = tokenizer.apply_chat_template(formatted_messages, tokenize=False, add_generation_prompt=True)
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.3,
            do_sample=True
        )
    
    response_text = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
    
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)