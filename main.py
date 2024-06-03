import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import uvicorn

class Mensagem(BaseModel):
    mensagem: str

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Carregar o modelo e o tokenizer pré-treinados
try:
    tokenizer = AutoTokenizer.from_pretrained('ai-forever/mGPT')
    modelo = AutoModelForCausalLM.from_pretrained('ai-forever/mGPT')
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
    raise

# Definir o token de preenchimento para ser o mesmo que o token de fim de sequência
tokenizer.pad_token = tokenizer.eos_token

@app.post('/responder')
async def responder(dados: Mensagem):
    try:
        logging.info(f"Recebido dados: {dados}")
        
        # Adicionar um prefixo à mensagem do usuário para indicar que é uma pergunta
        mensagem_com_prefixo = "Pergunta: " + dados.mensagem
        
        # Codificar a mensagem do usuário com prefixo e gerar uma resposta
        inputs = tokenizer.encode_plus(
            mensagem_com_prefixo,
            add_special_tokens=True,
            return_tensors='pt',
            padding='max_length',
            truncation=True,
            max_length=50, 
            return_attention_mask=True
        )
        
        logging.info(f"Inputs gerados: {inputs}")
        
        # Gerar uma resposta
        outputs = modelo.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_new_tokens=40, 
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        
        logging.info(f"Outputs gerados: {outputs}")
        
        # Decodificar a resposta, removendo o texto da entrada
        resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)
        resposta = resposta[len(mensagem_com_prefixo):].strip()
        
        logging.info(f"Resposta gerada: {resposta}")
        
        return JSONResponse(content={'resposta': resposta})
    except Exception as e:
        logging.error(f"Erro ao gerar resposta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host='0.0.0.0', port=8000)
