import os
from dotenv import load_dotenv

load_dotenv()

MEDICALSYS_BASE_URL = os.getenv("MEDICALSYS_BASE_URL", "").rstrip("/")

# Basic Auth
MEDICALSYS_BASIC_USER = os.getenv("MEDICALSYS_BASIC_USER", "").strip()
MEDICALSYS_BASIC_PASS = os.getenv("MEDICALSYS_BASIC_PASS", "").strip()

# Bearer/Token
MEDICALSYS_AUTH_HEADER = os.getenv("MEDICALSYS_AUTH_HEADER", "").strip()

# API Keys
MEDICALSYS_API_KEY_NAME = os.getenv("MEDICALSYS_API_KEY_NAME", "apikey").strip()
MEDICALSYS_API_KEY_VALUE = os.getenv("MEDICALSYS_API_KEY_VALUE", "").strip()

MEDICALSYS_API_KEY2_NAME = os.getenv("MEDICALSYS_API_KEY2_NAME", "msys-costumer-apikey").strip()
MEDICALSYS_API_KEY2_VALUE = os.getenv("MEDICALSYS_API_KEY2_VALUE", "").strip()

DEFAULT_CLINIC_ID = os.getenv("DEFAULT_CLINIC_ID")
DEFAULT_DOCTOR_ID = os.getenv("DEFAULT_DOCTOR_ID")

if not MEDICALSYS_BASE_URL:
    raise RuntimeError("MEDICALSYS_BASE_URL não configurado (.env).")