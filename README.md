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

Rota: /agenda

Método: GET

Parâmetros:

clinic_id: ID da clínica.

doctor_id: ID do médico.

date: Data do agendamento (formato YYYY-MM-DD).

Exemplo:

```bash
curl "http://localhost:5000/agenda?clinic_id=123&doctor_id=456&date=2025-08-12"
```

2. Criar Agendamento (POST)

Rota: /agenda

Método: POST

Parâmetros:

id_clinica: ID da clínica.

medico: ID do médico.

paciente: ID do paciente (ou paciente_provisorio caso não tenha ID).

momento: Data do agendamento (YYYY-MM-DD).

horario_inicio: Hora de início do agendamento (HH:MM).

horario_fim: Hora de fim do agendamento (HH:MM).

procedimentos_ids: Lista de IDs de procedimentos.

meio_de_pagamento: Meio de pagamento (espe, conv, cart, debi).

tel_celular: Número de telefone do paciente.

observacoes: Observações sobre o agendamento.

Exemplo:

```bash
curl -X POST "http://localhost:5000/agenda" \
  -H "Content-Type: application/json" \
  -d '{
        "id_clinica": "9",
        "medico": "652",
        "paciente": 13,
        "momento": "2025-08-12",
        "horario_inicio": "18:00",
        "horario_fim": "18:10",
        "meio_de_pagamento": "espe",
        "tel_celular": "83998335658",
        "procedimentos_ids": [12, 13],
        "observacoes": "Loren ipsum dollor."
      }'
```

3. Atualizar Agendamento (PUT)

Rota: /agenda/{id}

Método: PUT

Parâmetros:

Id do agendamento a ser atualizado.

Os parâmetros podem ser os mesmos do POST, mas apenas os que precisam ser alterados.

Exemplo:

```bash
curl -X PUT "http://localhost:5000/agenda/43033" \
  -H "Content-Type: application/json" \
  -d '{
        "momento": "2025-08-12",
        "horario_inicio": "18:00",
        "horario_fim": "18:10",
        "observacoes": "ajuste de horario"
      }'
```

4. Consultar Agendamento por ID (GET)

Rota: /agenda/{id}

Método: GET

Parâmetros: id (ID do agendamento).

Exemplo:

```bash
curl "http://localhost:5000/agenda/43033"
```

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

## 📝 Contribuindo

Clone o repositório.

Crie uma branch para sua feature:

git checkout -b minha-feature


Faça suas alterações e commit:

git commit -am 'Adiciona nova feature'


Push para sua branch:

git push origin minha-feature


Abra um pull request.

## 📜 Licença

Distribuído sob a licença MIT. Veja o arquivo LICENSE
 para mais informações.
