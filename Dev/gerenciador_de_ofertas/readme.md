
# 📦 Gerenciador de Ofertas

Um projeto **open source** desenvolvido em **Python** com **FastAPI** para monitorar preços de produtos e enviar alertas automáticos via Webhook.  
Criado como parte do meu portfólio de estudos em TI, este projeto é simples, extensível e ideal para quem deseja aprender sobre APIs modernas.

---

## 🚀 Como foi criado

- Estrutura organizada em **FastAPI** para criação de endpoints REST.
- Utilização de **Uvicorn** como servidor ASGI.
- Funções auxiliares em `utils/monitor.py` para:
  - Buscar preços em uma API externa.
  - Enviar alertas para Webhook (ex.: Discord, Slack).
- Configuração de variáveis sensíveis via **`.env`** com suporte de `python-dotenv`.
- Ambiente virtual isolado com **venv**.
- Testes automatizados com **pytest**.

---

## 📂 Estrutura do projeto

```
gerenciador_de_ofertas/
│── app.py
│── utils/
│   ├── monitor.py
│   └── __init__.py
│── tests/
│   └── test_app.py
│── .env
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── .gitignore
│── README.md
```

---

## ⚙️ Como utilizar

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/gerenciador_de_ofertas.git
cd gerenciador_de_ofertas
```

### 2. Criar ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.\.venv\Scripts\activate    # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz:
```env
WEBHOOK_URL=https://seu.webhook.url/aqui
API_PRODUTO_URL=https://api.exemplo.com/produto/001
PRECO_LIMITE=500.00
NOME_PRODUTO=Teclado Mecânico Super X
```

### 5. Rodar servidor
```bash
uvicorn app:app --reload
```

Acesse no navegador:
- `http://127.0.0.1:8000/preco` → consulta preço
- `http://127.0.0.1:8000/alerta` → envia alerta
- `http://127.0.0.1:8000/docs` → documentação interativa (Swagger UI)
- `http://127.0.0.1:8000/redoc` → documentação alternativa (Redoc)

---

## 🧪 Testes

Execute os testes com:
```bash
pytest
```

---

## 🌍 Open Source & Colaborações

Este projeto é **open source** e está aberto para melhorias.  
Sinta-se à vontade para abrir **issues**, enviar **pull requests** ou sugerir novas funcionalidades.  
Toda colaboração é bem-vinda! 💡

---

## 📜 Licença

Distribuído sob a licença MIT.  
Você pode usar, modificar e distribuir livremente, desde que mantenha os créditos.

---

## ✨ Autor

Desenvolvido por lorac-2 com 💖 como parte do portfólio de estudos em TI.
```

---


