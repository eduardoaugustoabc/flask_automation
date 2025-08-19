# Integração MedicalSys - Agenda

Expose localmente dois endpoints que consomem o Swagger "Integrações - Agenda":

- GET  /agenda     -> chama GET  {MEDICALSYS_BASE_URL}/agenda/
- POST /agenda     -> chama POST {MEDICALSYS_BASE_URL}/agenda/
- (o cliente também tem GET /agenda/{id}/ para uso interno)

## 1) Preparar ambiente

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

## 2) Configurar .env

Copie .env.example para .env e preencha:
- MEDICALSYS_BASE_URL (ex.: https://gateway.medicalsys.com.br:9000/integracoes)
- MEDICALSYS_AUTH_HEADER (ex.: "Bearer <token>" ou "Token <token>")

## 3) Rodar

python app.py

A API local sobe em http://localhost:5000

### Exemplos

Listar agenda (com filtros opcionais):
curl "http://localhost:5000/agenda?clinic_id=123&doctor_id=456&date=2025-08-12"

Criar agendamento:
curl -X POST "http://localhost:5000/agenda" \
  -H "Content-Type: application/json" \
  -d '{
        "clinic_id": 123,
        "doctor_id": 456,
        "patient_id": 987,
        "start": "2025-08-12T14:00:00-03:00",
        "end":   "2025-08-12T14:30:00-03:00",
        "notes": "Consulta retorno"
      }'
