from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

app = FastAPI(
    title="Gerenciador de Ofertas",
    description="API para consultar preços e enviar alertas de ofertas",
    version="1.0.0"
)

API_PRODUTO_URL = os.getenv("API_PRODUTO_URL", "https://fakestoreapi.com/products/1")
PRECO_LIMITE = float(os.getenv("PRECO_LIMITE", "500.0"))
NOME_PRODUTO = os.getenv("NOME_PRODUTO", "Produto de Teste")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")


# ✅ Modelo de resposta para /preco
class PrecoResponse(BaseModel):
    produto: str
    preco: float
    fonte: str
    timestamp: str


# ✅ Modelo de requisição para /alerta
class AlertaRequest(BaseModel):
    limite: float


# ✅ Modelo de resposta para /alerta
class AlertaResponse(BaseModel):
    status: str
    detalhe: dict | None = None
    preco: float | None = None
    limite: float | None = None


@app.get("/preco", response_model=PrecoResponse, responses={
    200: {
        "description": "Preço consultado com sucesso",
        "content": {
            "application/json": {
                "example": {
                    "produto": "Fjallraven - Foldsack No. 1 Backpack",
                    "preco": 109.95,
                    "fonte": "https://fakestoreapi.com/products/1",
                    "timestamp": "2025-11-25T00:35:00Z"
                }
            }
        }
    }
})
def consultar_preco():
    try:
        response = requests.get(API_PRODUTO_URL)
        response.raise_for_status()
        dados = response.json()

        preco = dados.get("price", 0.0)
        produto = dados.get("title", NOME_PRODUTO)

        return PrecoResponse(
            produto=produto,
            preco=preco,
            fonte=API_PRODUTO_URL,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerta", response_model=AlertaResponse, responses={
    200: {
        "description": "Resultado da verificação de alerta",
        "content": {
            "application/json": {
                "example": {
                    "status": "Alerta enviado",
                    "detalhe": {
                        "produto": "Fjallraven - Foldsack No. 1 Backpack",
                        "preco": 109.95,
                        "mensagem": "Preço abaixo do limite: 200.0",
                        "timestamp": "2025-11-25T00:40:00Z"
                    }
                }
            }
        }
    }
})
def enviar_alerta(req: AlertaRequest):
    try:
        response = requests.get(API_PRODUTO_URL)
        response.raise_for_status()
        dados = response.json()

        preco = dados.get("price", 0.0)
        produto = dados.get("title", NOME_PRODUTO)

        limite = req.limite if req.limite else PRECO_LIMITE

        if preco <= limite and WEBHOOK_URL:
            alerta = {
                "produto": produto,
                "preco": preco,
                "mensagem": f"Preço abaixo do limite: {limite}",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            requests.post(WEBHOOK_URL, json=alerta)
            return {"status": "Alerta enviado", "detalhe": alerta}
        else:
            return {"status": "Sem alerta", "preco": preco, "limite": limite}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))