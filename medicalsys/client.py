# medicalsys/client.py
import requests
from requests.auth import HTTPBasicAuth
from typing import Any, Dict, Optional, Union, List, Tuple
from .config import (
    MEDICALSYS_BASE_URL,
    MEDICALSYS_BASIC_USER, MEDICALSYS_BASIC_PASS,
    MEDICALSYS_AUTH_HEADER,
    MEDICALSYS_API_KEY_NAME, MEDICALSYS_API_KEY_VALUE,
    MEDICALSYS_API_KEY2_NAME, MEDICALSYS_API_KEY2_VALUE,
)

class MedicalSysError(RuntimeError):
    pass

class MedicalSysClient:
    def __init__(self, timeout: int = 20, verify_tls: bool = True):
        self.base = MEDICALSYS_BASE_URL
        self.timeout = timeout
        self.verify = verify_tls
        self.session = requests.Session()

        if MEDICALSYS_BASIC_USER and MEDICALSYS_BASIC_PASS:
            self.session.auth = HTTPBasicAuth(MEDICALSYS_BASIC_USER, MEDICALSYS_BASIC_PASS)
        if MEDICALSYS_AUTH_HEADER:
            self.session.headers.update({"Authorization": MEDICALSYS_AUTH_HEADER})
        if MEDICALSYS_API_KEY_VALUE:
            self.session.headers.update({MEDICALSYS_API_KEY_NAME: MEDICALSYS_API_KEY_VALUE})
        if MEDICALSYS_API_KEY2_VALUE:
            self.session.headers.update({MEDICALSYS_API_KEY2_NAME: MEDICALSYS_API_KEY2_VALUE})

        self.session.headers.update({"Accept": "application/json"})

    def _request_with_slash_fallback(self, method: str, path: str, **kwargs):
        url = f"{self.base}{path}"
        r = self.session.request(method, url, timeout=self.timeout, verify=self.verify, **kwargs)
        if r.status_code == 404:
            alt_path = path[:-1] if path.endswith("/") else path + "/"
            alt_url = f"{self.base}{alt_path}"
            r2 = self.session.request(method, alt_url, timeout=self.timeout, verify=self.verify, **kwargs)
            if r2.status_code != 404:
                return r2
        return r

    def get_agenda(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        r = self._request_with_slash_fallback("GET", "/agenda/", params=params)
        if r.status_code == 401:
            raise MedicalSysError("401 Unauthorized (verifique chaves/credenciais).")
        if not r.ok:
            raise MedicalSysError(f"Erro {r.status_code} em GET /agenda: {r.text}")
        return r.json() if r.text else {}

    def get_agendamento(self, agendamento_id: Union[int, str]) -> Dict[str, Any]:
        r = self._request_with_slash_fallback("GET", f"/agenda/{agendamento_id}/")
        if not r.ok:
            raise MedicalSysError(f"Erro {r.status_code} em GET /agenda/{agendamento_id}: {r.text}")
        return r.json() if r.text else {}

    def _to_form_pairs(self, payload: Dict[str, Any]) -> List[Tuple[str, str]]:
        pairs: List[Tuple[str, str]] = []
        for k, v in payload.items():
            if v is None:
                continue
            if isinstance(v, (list, tuple, set)):
                for item in v:
                    pairs.append((k, str(item)))
            else:
                pairs.append((k, str(v)))
        return pairs

    def create_agendamento(self, form_payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        form_pairs = self._to_form_pairs(form_payload)
        r = self._request_with_slash_fallback("POST", "/agenda/", data=form_pairs, headers=headers)
        if r.status_code == 400:
            raise MedicalSysError(f"400 Bad Request: {r.text}")
        if r.status_code == 401:
            raise MedicalSysError("401 Unauthorized (verifique chaves/credenciais).")
        if not r.ok:
            raise MedicalSysError(f"Erro {r.status_code} em POST /agenda: {r.text}")
        return r.json() if r.text else {}
        
    # PUT /agenda/{id}/  (FORM DATA!)
    def update_agendamento(self, agendamento_id: Union[int, str], form_payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        form_pairs = self._to_form_pairs(form_payload)  # mesma função usada no POST
        r = self._request_with_slash_fallback("PUT", f"/agenda/{agendamento_id}/", data=form_pairs, headers=headers)
        if r.status_code == 400:
            raise MedicalSysError(f"400 Bad Request: {r.text}")
        if r.status_code == 401:
            raise MedicalSysError("401 Unauthorized (verifique chaves/credenciais).")
        if not r.ok:
            raise MedicalSysError(f"Erro {r.status_code} em PUT /agenda/{agendamento_id}: {r.text}")
        return r.json() if r.text else {}
