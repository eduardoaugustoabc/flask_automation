# Integração com MedicalSys - Sistema de Agendamento

Este repositório contém a implementação de um microserviço em Flask para integração com a API de Agendamento do MedicalSys. Ele permite a criação, atualização e consulta de agendamentos para clínicas e médicos, com funcionalidades como a gestão de pacientes, horários e procedimentos.

## 🚀 Início Rápido

### Clone o repositório:
```bash
git clone https://github.com/SEU-USUARIO/medicalsys_integration.git
cd medicalsys_integration
```
## Instale as dependências:

Certifique-se de ter o pip instalado e, em seguida, instale as dependências do projeto.
```bash
pip install -r requirements.txt
```

## Configure o arquivo .env:

Crie um arquivo .env na raiz do repositório com as configurações necessárias para a integração com a API do MedicalSys.

Exemplo de .env:

```bash
MEDICALSYS_BASE_URL=https://gateway.medicalsys.com.br:9000/integracoes
MEDICALSYS_BASIC_USER=SEU_USER
MEDICALSYS_BASIC_PASS=SUA_SENHA
MEDICALSYS_API_KEY_NAME=apikey
MEDICALSYS_API_KEY_VALUE=SUA_API_KEY
MEDICALSYS_API_KEY2_NAME=msys-costumer-apikey
MEDICALSYS_API_KEY2_VALUE=SUA_API_KEY2
```

Certifique-se de preencher com as credenciais da sua conta MedicalSys (API Key e, se necessário, Basic Auth).

## Execute o serviço localmente:

Inicie o servidor Flask para testar a integração localmente.

```bash
python app.py
```

O servidor estará disponível em http://localhost:5000.

## 🧩 Funcionalidades
## 1. Consultar Agendamentos (GET)

## 2. Criar Agendamento (POST)

## 3. Atualizar Agendamento (PUT)

## 4. Consultar Agendamento por ID (GET)

## 🛠️ Estrutura de Arquivos
```bash
.
├── app.py                # Arquivo principal da aplicação Flask
├── medicalsys/           # Lógica da integração com o MedicalSys
│   ├── client.py         # Cliente para interagir com a API MedicalSys
│   ├── agenda_service.py # Funções para lidar com agendamentos
│   └── config.py         # Arquivo de configuração (.env)
├── requirements.txt      # Dependências do projeto
└── .env                  # Variáveis de ambiente (API Keys, URLs)
```

## 📦 Dependências

Flask: Microframework para criar a API.

Requests: Biblioteca para fazer chamadas HTTP.

python-dotenv: Para carregar variáveis de ambiente do arquivo .env.

json: Para manipulação de JSON.
