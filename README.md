## Bot Bancário Discord – Desafio Rede Meia‑Noite

Bot Discord que simula um sistema bancário simples entre usuários, implementado em **Python** com foco em **Clean Code**, **tratamento de erros** e **persistência de dados**.

---

## 🔹 Objetivo do Projeto

Atender aos requisitos do desafio:

- **/saldo**: retorna o saldo atual do usuário (todos começam com **100 moedas**).
- **/transferir @usuário valor**:
  - Debita do remetente e credita o destinatário.
  - Impede saldo insuficiente.
  - Impede valores negativos ou zero.
  - Impede transferências para si mesmo.
  - Persiste os dados em disco para não perder saldo ao reiniciar o bot.

---

## 🚀 Funcionalidades Principais

- **Sistema bancário simples** entre usuários do Discord.
- **Comando `/saldo`**:
  - Retorna o saldo atual do usuário em um **Embed**.
  - Inicializa automaticamente o usuário com **100 moedas** na primeira utilização.
- **Comando `/transferir`**:
  - Transfere moedas entre usuários utilizando **slash command**.
  - Exibe resultado e novo saldo em **Embed de sucesso**.
- **Persistência em arquivo JSON**:
  - Todos os saldos são salvos em `data/users.json`.
  - O arquivo é criado automaticamente, se não existir.
- **Tratamento de erros amigável**:
  - Valores inválidos (texto no lugar de número, número ≤ 0).
  - Saldo insuficiente.
  - Transferência para si mesmo.
  - Erros de banco de dados.
  - Todas as respostas de erro são enviadas em **Embeds**.
- **Segurança**:
  - Token do bot e prefixo configurados via `.env`.

---

## 📋 Pré‑requisitos

- **Python 3.8+**
- Uma conta no **Discord Developer Portal** com um bot criado
- Biblioteca `discord.py` (instalada via `requirements.txt`)

---

## 🔧 Instalação e Configuração

1. **Instalar dependências**

   Na raiz do projeto:

   ```bash
   pip install -r requirements.txt
   ```

2. **Criar arquivo de variáveis de ambiente**

   Use o modelo `env.example` e crie um arquivo `.env` na raiz:

   ```text
   DISCORD_TOKEN=seu_token_do_bot_aqui
   DISCORD_PREFIX=/
   ```

3. **Configurar o bot no Discord**

   - Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
   - Crie uma aplicação ou selecione uma existente.
   - Vá em **“Bot”**, gere e copie o **Token**.
   - Cole o token no `.env` em `DISCORD_TOKEN`.

4. **Convidar o bot para o servidor**

   - No Developer Portal, vá em **“OAuth2” → “URL Generator”**.
   - Marque os escopos: **`bot`** e **`applications.commands`**.
   - Em permissões do bot, selecione:
     - **Send Messages**
     - **Embed Links**
     - **Use Slash Commands**
   - Acesse a URL gerada e adicione o bot ao seu servidor.

5. **Executar o bot**

   Na raiz do projeto:

   ```bash
   python main.py
   ```

   Ao iniciar, o bot:
   - Carrega o banco de dados JSON.
   - Registra os comandos `/saldo` e `/transferir`.
   - Exibe no console em quantos servidores está e qual prefixo está usando.

---

## 🎮 Uso dos Comandos

### `/saldo`

Consulta o saldo atual do usuário.

```text
/saldo
```

- Retorna um **Embed** com:
  - Nome do usuário.
  - Saldo atual em moedas.

### `/transferir`

Transfere moedas para outro usuário.

```text
/transferir usuario:@usuario valor:50
```

- **Parâmetros**:
  - `usuario`: menção ao usuário que receberá as moedas.
  - `valor`: quantidade de moedas (número positivo).

- **Regras de validação**:
  - ❌ Não permite valores **negativos** ou **zero**.
  - ❌ Não permite transferência **para si mesmo**.
  - ❌ Não permite transferência com **saldo insuficiente**.
  - ❌ Não aceita texto no lugar de número (exibe mensagem amigável).
  - ✅ Todas as mensagens de erro são exibidas em **Embeds**.

---

## 📁 Estrutura do Projeto

```text
teste-meianoite/
├── bot/
│   ├── __init__.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── saldo.py          # Comando /saldo
│   │   └── transferir.py     # Comando /transferir
│   ├── database/
│   │   ├── __init__.py
│   │   └── manager.py        # Gerenciador de persistência (JSON)
│   └── utils/
│       ├── __init__.py
│       └── errors.py         # Erros customizados e Embeds de erro
├── data/
│   └── users.json            # Banco de dados de saldos (criado em runtime)
├── main.py                   # Ponto de entrada do bot
├── requirements.txt          # Dependências Python
├── env.example               # Exemplo de configuração de ambiente
└── README.md
```

---

## 🏗️ Arquitetura e Clean Code

- **Separação de responsabilidades**:
  - `commands/`: lógica dos comandos `/saldo` e `/transferir`.
  - `database/manager.py`: leitura/escrita de saldos em JSON.
  - `utils/errors.py`: definição de exceções de domínio e conversão para Embeds.
  - `main.py`: inicialização do bot, carregamento de Cogs e sincronização de slash commands.
- **Tratamento de erros centralizado**:
  - Cada comando captura `BankingError` (erros de domínio) e converte para mensagens amigáveis.
  - Exceções inesperadas também são tratadas e comunicadas ao usuário sem derrubar o bot.
- **Persistência desacoplada**:
  - A lógica de negócio não conhece detalhes de como o JSON é salvo.
  - Facilita trocar o backend para SQLite no futuro, se necessário.
- **Configuração via ambiente**:
  - Token e prefixo não ficam hardcoded no código-fonte.

---

## 🔒 Segurança

- **Token do bot**:
  - Nunca é commitado; é lido via variável de ambiente `DISCORD_TOKEN`.
  - `.env` deve ser mantido apenas localmente.
- **Validações de entrada**:
  - Conversão explícita e protegida de string para número no comando `/transferir`.
  - Bloqueio de operações inválidas com mensagens claras.
- **Resiliência**:
  - Erros de I/O ou JSON no banco de dados são encapsulados em `DatabaseError`.
  - O bot não “crasha” em caso de entrada inválida do usuário.

---

## 🐛 Troubleshooting Rápido

- **Bot não responde aos comandos**:
  - Verifique se o bot está **online** no Discord.
  - Confira se o **token** no `.env` está correto.
  - Confirme se o bot tem permissão de **“Use Slash Commands”** e **“Send Messages”**.
  - Aguarde alguns segundos após o primeiro start para os slash commands sincronizarem.

- **Erro de acesso ao banco de dados (JSON)**:
  - Verifique se a pasta `data/` existe e permite escrita.
  - Verifique se o arquivo `data/users.json` não está corrompido (pode apagá‑lo e deixar o bot recriar).

---

## 📄 Observação Final

Este projeto foi desenvolvido especificamente para o **desafio da Rede Meia‑Noite**, priorizando:
- Código organizado e modular.
- Tratamento robusto de erros.
- Persistência simples, porém confiável, em arquivo JSON.
