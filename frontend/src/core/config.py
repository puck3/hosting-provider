import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_CONFIG = {
    "backend_host": os.getenv("BACKEND_HOST", "localhost"),
    "backend_port": os.getenv("BACKEND_PORT", "8000"),
}

BACKEND_URL = f"http://{BACKEND_CONFIG['backend_host']}:{BACKEND_CONFIG['backend_port']}"
