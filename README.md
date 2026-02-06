# Azure AI-102 Evaluator Web App

Aplicativo web para interagir com um avaliador oficial da certificação Microsoft **AI-102** usando Azure OpenAI (gpt-5-mini) com sistema de prompts especializado.

## 🎯 Características

- ✅ Avaliador oficial de AI-102 em português
- ✅ Interface web moderna e responsiva
- ✅ Chat em tempo real com modelo GPT-5-mini
- ✅ Sem autenticação - compartilhe o link
- ✅ Sistema prompt customizado para exame
- ✅ Suporte para até 20.000 tokens
- ✅ Integração com Azure OpenAI

## 📋 Pré-requisitos

- Python 3.13+
- Chave de API do Azure OpenAI
- Endpoint do Azure OpenAI

## 🚀 Instalação Local

### 1. Clone ou copie o projeto

```bash
cd Agent
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo .env

```dotenv
AZURE_ENDPOINT=https://<seu-recurso>.openai.azure.com/openai/v1
AZURE_API_KEY=<sua-chave-api>
AZURE_DEPLOYMENT_ID=gpt-5-mini-2
AZURE_API_VERSION=

USE_AI102_SYSTEM_PROMPT=true

HOST=0.0.0.0
PORT=8000
```

### 5. Execute a aplicação

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse em: http://localhost:8000

## 📦 Deploy no Azure App Service

### Opção A: Portal do Azure (Recomendado para iniciantes)

1. **Criar App Service**
   - Vá para Azure Portal
   - Crie novo App Service (Python 3.13, Linux)
   - Copie os arquivos do projeto para o repositório

2. **Configurar Variáveis de Ambiente**
   - No App Service → Configuration → Application settings
   - Adicione as variáveis:
     - `AZURE_ENDPOINT`
     - `AZURE_API_KEY`
     - `AZURE_DEPLOYMENT_ID`
     - `USE_AI102_SYSTEM_PROMPT=true`
     - `WEBSITES_PORT=8000`

3. **Reiniciar o App Service**

### Opção B: Azure CLI (Avançado)

```bash
# Login no Azure
az login

# Criar Resource Group
az group create --name ai-evaluator-rg --location brazilsouth

# Criar App Service Plan
az appservice plan create \
  --name ai-evaluator-plan \
  --resource-group ai-evaluator-rg \
  --sku B1 \
  --is-linux

# Criar App Service
az webapp create \
  --resource-group ai-evaluator-rg \
  --plan ai-evaluator-plan \
  --name ai-evaluator-app \
  --runtime "PYTHON|3.13"

# Configurar variáveis
az webapp config appsettings set \
  --name ai-evaluator-app \
  --resource-group ai-evaluator-rg \
  --settings \
    AZURE_ENDPOINT="https://<seu-recurso>.openai.azure.com/openai/v1" \
    AZURE_API_KEY="<sua-chave-api>" \
    AZURE_DEPLOYMENT_ID="gpt-5-mini-2" \
    USE_AI102_SYSTEM_PROMPT="true" \
    WEBSITES_PORT="8000"

# Deploy via ZIP
zip -r deploy.zip . -x ".venv/*" "__pycache__/*" ".git/*"
az webapp deployment source config-zip \
  --resource-group ai-evaluator-rg \
  --name ai-evaluator-app \
  --src deploy.zip
```

### Opção C: GitHub Actions (CI/CD Automático)

1. **Push para GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/seu-repo.git
   git push -u origin main
   ```

2. **Configurar Secrets no GitHub**
   - Vá para Settings → Secrets and variables → Actions
   - Adicione:
     - `AZURE_APP_SERVICE_NAME`: nome do seu App Service
     - `AZURE_APP_SERVICE_PUBLISH_PROFILE`: perfil de publicação do Azure

3. **Deploy Automático**
   - Qualquer push para `main` dispara o workflow
   - Veja em Actions → Workflows

## 🔗 API Endpoints

### GET `/`
Página HTML principal da avaliadora

### GET `/health`
Status de saúde da aplicação
```json
{
  "status": "healthy",
  "agent_ready": true
}
```

### POST `/api/chat`
Enviar mensagem e obter resposta

**Request:**
```json
{
  "content": "Sua pergunta para o avaliador"
}
```

**Response:**
```json
{
  "message": "Resposta da avaliadora",
  "success": true,
  "error": null
}
```

### GET `/api/config`
Obter configuração do frontend

## 📁 Estrutura do Projeto

```
Agent/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI servidor principal
│   ├── agent.py          # Cliente OpenAI
│   └── config.py         # Carregamento de configurações
├── static/
│   ├── index.html        # Interface web
│   ├── style.css         # Estilos CSS
│   └── script.js         # JavaScript cliente
├── system_prompt.py      # Prompt do sistema para AI-102
├── requirements.txt      # Dependências Python
├── .env                  # Variáveis de ambiente locais
├── startup.py            # Script de inicialização para Azure
├── Procfile              # Configuração para Heroku/Azure
├── .deployment           # Configuração de deployment
└── .github/
    └── workflows/
        └── deploy.yml    # GitHub Actions CI/CD
```

## 🔐 Segurança

- ✅ **Sem autenticação na interface** - Qualquer pessoa com o link pode acessar
- ✅ **Chave API segura** - Nunca é exposta ao navegador
- ✅ **HTTPS obrigatório** - Em produção no Azure
- ✅ **Logging** - Disponível no Application Insights
- ⚠️ **Não use em dados sensíveis** - Sem criptografia ponta-a-ponta

## 🐛 Troubleshooting

### Erro: "No assistant response found"
- Aumentar `max_tokens` em `app/agent.py`
- Verificar se a chave API é válida
- Verificar os logs no Azure Portal

### Erro: "AZURE_ENDPOINT not found"
- Confirmar que `.env` existe no diretório raiz
- Verificar variáveis de ambiente no App Service

### Erro: "Connection refused"
- Verificar se o servidor está rodando
- Confirmar porta 8000 está aberta

### Resposta truncada ou vazia
- Max tokens já está em 20.000 (suficiente)
- Aumentar se necessário modificando `app/agent.py`
- Verificar logs para detalhes

## 📞 Referências

- [Azure App Service Docs](https://learn.microsoft.com/en-us/azure/app-service/)
- [Azure OpenAI Docs](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python in Azure](https://learn.microsoft.com/en-us/azure/python/)

## 📄 Licença

MIT License

---

**Versão:** 1.0  
**Última atualização:** Fevereiro 2026  
**Desenvolvido com:** FastAPI, Azure OpenAI, Python 3.13
