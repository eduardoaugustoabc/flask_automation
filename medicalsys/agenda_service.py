# medicalsys/agenda_service.py
from typing import Dict, Any, Optional, List, Tuple, Union
from datetime import datetime
from .client import MedicalSysClient
from .client import MedicalSysClient
from .config import DEFAULT_CLINIC_ID, DEFAULT_DOCTOR_ID

client = MedicalSysClient()

def _iso_to_date_time(iso_str: str):
    """'2025-08-12T14:00:00-03:00' -> ('2025-08-12','14:00')"""
    dt = datetime.fromisoformat(str(iso_str).replace("Z", "+00:00"))
    return dt.date().isoformat(), dt.strftime("%H:%M")

def _map_meio_pagamento(value: str) -> str:
    if not value:
        return value
    v = str(value).strip().lower()
    aliases = {
        "cart": "cart", "cartao": "cart", "cartão": "cart", "credito": "cart", "crédito": "cart",
        "debi": "debi", "debito": "debi", "débito": "debi",
        "espe": "espe", "especie": "espe", "espécie": "espe", "dinheiro": "espe",
        "conv": "conv", "convenio": "conv", "convênio": "conv",
    }
    return aliases.get(v, v)

def _normalize_payload_to_form(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte o JSON recebido no nosso /agenda para o form exigido pelo MedicalSys.
    Retorna um dict de strings pronto para x-www-form-urlencoded.
    (client.create_agendamento cuidará de listas/tuplas)
    """
    out: Dict[str, Any] = {}

    # Clínica (enviar ambos nomes: id_clinica e clinica_id)
    id_cli = dados.get("id_clinica") or dados.get("clinica_id") or dados.get("clinic_id")
    if id_cli is not None:
        out["id_clinica"] = str(id_cli)
        out["clinica_id"] = str(id_cli)

    # Médico (enviar ambos nomes: medico e medico_id)
    med = dados.get("medico") or dados.get("medico_id") or dados.get("doctor_id")
    if med is not None:
        out["medico"] = str(med)
        out["medico_id"] = str(med)

    # Paciente (um dos dois é obrigatório)
    if dados.get("paciente") is not None:
        out["paciente"] = str(dados["paciente"])
    elif dados.get("paciente_id") is not None:
        out["paciente"] = str(dados["paciente_id"])
    elif dados.get("patient_id") is not None:
        out["paciente"] = str(dados["patient_id"])
    elif dados.get("paciente_provisorio"):
        out["paciente_provisorio"] = str(dados["paciente_provisorio"])

    # Datas/horas
    if all(k in dados for k in ("momento","horario_inicio","horario_fim")):
        out["momento"] = str(dados["momento"])
        out["horario_inicio"] = str(dados["horario_inicio"])
        out["horario_fim"] = str(dados["horario_fim"])
    elif "start" in dados and "end" in dados:
        data, h_ini = _iso_to_date_time(dados["start"])
        _,    h_fim = _iso_to_date_time(dados["end"])
        out["momento"] = data
        out["horario_inicio"] = h_ini
        out["horario_fim"] = h_fim

    # Pagamento e telefone
    meio = dados.get("meio_de_pagamento") or dados.get("payment") or dados.get("pagamento")
    out["meio_de_pagamento"] = _map_meio_pagamento(meio) if meio else None

    tel = dados.get("tel_celular") or dados.get("telefone") or dados.get("celular") or dados.get("phone")
    if tel:
        out["tel_celular"] = str(tel)

    # Observações
    if "observacoes" in dados:
        out["observacoes"] = str(dados["observacoes"])
    elif "notes" in dados:
        out["observacoes"] = str(dados["notes"])

    # Procedimentos
    procs = dados.get("procedimentos_ids") or dados.get("procedure_ids") or dados.get("procedimentos")
    if procs is not None:
        # o client vai transformar listas em chaves repetidas
        out["procedimentos_ids"] = procs

    # Validação mínima (deixa mensagem clara antes de bater no gateway)
    missing = []
    for k in ("momento","horario_inicio","horario_fim","meio_de_pagamento","tel_celular"):
        if not out.get(k):
            missing.append(k)
    if not out.get("id_clinica"):
        missing.append("id_clinica/clinica_id")
    if not out.get("medico"):
        missing.append("medico/medico_id")
    if "paciente" not in out and "paciente_provisorio" not in out:
        missing.append("paciente|paciente_provisorio")
    if "procedimentos_ids" not in out or not out["procedimentos_ids"]:
        missing.append("procedimentos_ids")

    if missing:
        raise ValueError("Payload incompleto/ inválido: " + ", ".join(missing))

    return out

def listar_agenda(filtros: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return client.get_agenda(dict(filtros) if filtros else {})

def criar_agendamento(dados: Dict[str, Any]) -> Dict[str, Any]:
    form = _normalize_payload_to_form(dados)
    return client.create_agendamento(form)

# --- opcional (debug): veja o form final sem chamar o gateway ---
def debug_normalize(dados: Dict[str, Any]) -> Dict[str, Any]:
    return _normalize_payload_to_form(dados)

def _normalize_update_to_form(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Versão 'leniente' para UPDATE:
    - mapeia nomes amigáveis -> nomes do Swagger
    - NÃO exige todos os campos (envia só os presentes)
    - mantém a regra: se vier 'paciente' ou 'paciente_provisorio', repassa
    """
    out: Dict[str, Any] = {}

    # clínica (mandamos ambas variantes para compatibilidade)
    id_cli = dados.get("id_clinica") or dados.get("clinica_id") or dados.get("clinic_id")
    if id_cli is not None:
        out["id_clinica"] = str(id_cli)
        out["clinica_id"] = str(id_cli)

    # médico
    med = dados.get("medico") or dados.get("medico_id") or dados.get("doctor_id")
    if med is not None:
        out["medico"] = str(med)
        out["medico_id"] = str(med)

    # paciente (opcionais – envie se mudar)
    if dados.get("paciente") is not None:
        out["paciente"] = str(dados["paciente"])
    elif dados.get("paciente_id") is not None:
        out["paciente"] = str(dados["paciente_id"])
    elif dados.get("patient_id") is not None:
        out["paciente"] = str(dados["patient_id"])
    if dados.get("paciente_provisorio"):
        out["paciente_provisorio"] = str(dados["paciente_provisorio"])

    # datas/horas – aceite já separados ou start/end ISO
    if "momento" in dados:
        out["momento"] = str(dados["momento"])
    if "horario_inicio" in dados:
        out["horario_inicio"] = str(dados["horario_inicio"])
    if "horario_fim" in dados:
        out["horario_fim"] = str(dados["horario_fim"])
    if "start" in dados:
        data, h_ini = _iso_to_date_time(dados["start"])
        out.setdefault("momento", data)
        out.setdefault("horario_inicio", h_ini)
    if "end" in dados:
        _, h_fim = _iso_to_date_time(dados["end"])
        out.setdefault("horario_fim", h_fim)

    # pagamento/telefone/obs
    if "meio_de_pagamento" in dados or "payment" in dados or "pagamento" in dados:
        meio = dados.get("meio_de_pagamento") or dados.get("payment") or dados.get("pagamento")
        out["meio_de_pagamento"] = _map_meio_pagamento(meio)
    if "tel_celular" in dados or "telefone" in dados or "celular" in dados or "phone" in dados:
        tel = dados.get("tel_celular") or dados.get("telefone") or dados.get("celular") or dados.get("phone")
        out["tel_celular"] = str(tel)
    if "observacoes" in dados:
        out["observacoes"] = str(dados["observacoes"])
    if "notes" in dados:
        out["observacoes"] = str(dados["notes"])

    # procedimentos (lista)
    procs = (dados.get("procedimentos_ids")
             or dados.get("procedure_ids")
             or dados.get("procedimentos"))
    if procs is not None:
        out["procedimentos_ids"] = procs

    return out

def _extract_id(value):
    """Aceita int/str/dict({'id':...}) e retorna o id como string, se existir."""
    if value is None:
        return None
    if isinstance(value, dict):
        v = value.get("id") or value.get("Id") or value.get("ID")
        return str(v) if v is not None else None
    return str(value)

def _extract_proc_ids(current: Dict[str, Any]) -> List[int]:
    # tenta vários formatos comuns: 'procedimentos' como lista de objetos, ou já ids
    if "procedimentos_ids" in current and isinstance(current["procedimentos_ids"], list):
        return [int(x) for x in current["procedimentos_ids"] if isinstance(x, (int, str)) and str(x).isdigit()]
    procs = current.get("procedimentos") or []
    ids: List[int] = []
    for p in procs:
        if isinstance(p, dict) and ("id" in p):
            try:
                ids.append(int(p["id"]))
            except Exception:
                pass
    return ids

def _prefill_required_from_existing(agendamento_id: Union[int, str], form: Dict[str, Any]) -> Dict[str, Any]:
    """Completa campos obrigatórios a partir do GET /agenda/{id}/ e defaults."""
    try:
        current = client.get_agendamento(agendamento_id) or {}
    except Exception:
        current = {}

    # --- clínica ---
    cli = form.get("id_clinica") or form.get("clinica_id")
    if not cli:
        cli = (current.get("id_clinica") or current.get("clinica_id") or
               _extract_id(current.get("clinica")) or DEFAULT_CLINIC_ID)
        if cli:
            form["id_clinica"] = str(cli)
            form["clinica_id"] = str(cli)

    # --- médico ---
    med = form.get("medico") or form.get("medico_id")
    if not med:
        med = (_extract_id(current.get("medico")) or current.get("medico_id") or DEFAULT_DOCTOR_ID)
        if med:
            form["medico"] = str(med)
            form["medico_id"] = str(med)

    # --- procedimentos ---
    if not form.get("procedimentos_ids"):
        ids = _extract_proc_ids(current)
        if ids:
            form["procedimentos_ids"] = ids

    # --- telefone (algumas instâncias exigem) ---
    if "tel_celular" not in form and current.get("tel_celular"):
        form["tel_celular"] = str(current["tel_celular"])

    return form

def atualizar_agendamento(agendamento_id: Union[int, str], dados: Dict[str, Any]) -> Dict[str, Any]:
    form = _normalize_update_to_form(dados)  # já existente
    form = _prefill_required_from_existing(agendamento_id, form)

    # validação mínima (o backend está exigindo estes 3)
    missing = []
    if not (form.get("id_clinica") or form.get("clinica_id")):
        missing.append("id_clinica/clinica_id")
    if not (form.get("medico") or form.get("medico_id")):
        missing.append("medico/medico_id")
    # não bloqueia por falta de procedimentos_ids; deixa o backend validar
    if missing:
        raise ValueError("Payload incompleto para UPDATE: " + ", ".join(missing))

    return client.update_agendamento(agendamento_id, form)
