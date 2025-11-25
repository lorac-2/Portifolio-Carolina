import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_PRODUTO_URL = os.getenv("API_PRODUTO_URL")
PRECO_LIMITE = float(os.getenv("PRECO_LIMITE", "0"))
NOME_PRODUTO = os.getenv("NOME_PRODUTO", "Produto")

def _validar_config():
    faltantes = []
    if not WEBHOOK_URL:
        faltantes.append("WEBHOOK_URL")
    if not API_PRODUTO_URL:
        faltantes.append("API_PRODUTO_URL")
    if PRECO_LIMITE == 0:
        faltantes.append("PRECO_LIMITE")
    if not NOME_PRODUTO:
        faltantes.append("NOME_PRODUTO")
    if faltantes:
        return {
            "erro": "Configuração ausente",
            "faltantes": faltantes,
            "msg": "Verifique seu arquivo .env"
        }
    return None


def buscar_preco_na_api():
    """
    Consulta a API externa e retorna preço e dados básicos.
    Espera que a resposta contenha ao menos a chave 'preco'.
    """
    conf_erro = _validar_config()
    if conf_erro:
        return conf_erro

    try:
        resp = requests.get(API_PRODUTO_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Ajuste conforme o formato real da sua API
        preco = float(data.get("preco", 0))
        return {
            "produto": NOME_PRODUTO,
            "preco": preco,
            "fonte": API_PRODUTO_URL,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except requests.RequestException as e:
        return {
            "erro": "Falha ao consultar API",
            "detalhe": str(e),
            "fonte": API_PRODUTO_URL
        }
    except (ValueError, TypeError):
        return {
            "erro": "Formato inesperado da resposta da API",
            "fonte": API_PRODUTO_URL,
            "observacao": "Não foi possível converter 'preco' para número."
        }


def enviar_alerta_webhook():
    """
    Envia um alerta para o webhook quando o preço está <= PRECO_LIMITE.
    Retorna o status da operação.
    """
    conf_erro = _validar_config()
    if conf_erro:
        return conf_erro

    info = buscar_preco_na_api()
    if "erro" in info:
        return info

    preco = float(info.get("preco", 0))

    if preco <= PRECO_LIMITE:
        mensagem = (
            f"🔔 Oferta encontrada!\n"
            f"Produto: {NOME_PRODUTO}\n"
            f"Preço: R${preco:.2f}\n"
            f"Limite: R${PRECO_LIMITE:.2f}\n"
            f"Data: {datetime.utcnow().isoformat()}Z"
        )
        payload = {"content": mensagem}

        try:
            r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
            r.raise_for_status()
            return {"status": "alerta enviado", "preco": preco, "limite": PRECO_LIMITE}
        except requests.RequestException as e:
            return {"erro": "Falha ao enviar webhook", "detalhe": str(e)}
    else:
        return {
            "status": "preço acima do limite",
            "preco": preco,
            "limite": PRECO_LIMITE
        }