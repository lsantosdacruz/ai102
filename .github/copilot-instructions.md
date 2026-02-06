# Azure Foundry AI Agent Chat Web App

Aplicativo web simples para interagir com um agente de IA do Azure Foundry usando modelo GPT da OpenAI.

## ✅ Status de Configuração

- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions (não aplicável)
- [x] Compile the Project
- [x] Create and Run Task
- [x] Launch the Project
- [x] Ensure Documentation is Complete

## 🎯 Projeto Concluído!

O aplicativo web está **100% funcional** e rodando em http://localhost:8000

### Projeto Criado

```
Agent/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI servidor
│   ├── config.py         # Configurações
│   └── agent.py          # Agente de IA
├── static/
│   ├── index.html        # Interface web
│   ├── style.css         # Estilos modernos
│   └── script.js         # JavaScript
├── .env                  # Credenciais (configurar)
├── requirements.txt      # Dependências
└── README.md             # Documentação
```

### 🚀 Como Usar

1. **Configurar Azure Foundry** - Editar `.env`:
   ```
   AZURE_ENDPOINT=https://seu-foundry.openai.azure.com/
   AZURE_API_KEY=sua_chave_aqui
   AZURE_DEPLOYMENT_ID=seu_deployment_aqui
   ```

2. **Servidor já está rodando** - Acesse: http://localhost:8000

3. **Compartilhar** - O link funciona para qualquer pessoa (sem autenticação)

### 📋 Tecnologias

- **Backend**: FastAPI + Uvicorn
- **Frontend**: HTML5 + CSS3 + JavaScript
- **AI**: Azure Foundry GPT
- **Python**: 3.13
