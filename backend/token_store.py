import json
import os
from pathlib import Path

# 🔄 Makes the path dynamic no matter where the app runs (Windows, Linux, Render cloud)
BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "tokens.json"

def save_tokens(access_token, refresh_token, realm_id):
    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "realm_id": realm_id
    }
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

def load_tokens():
    if not TOKEN_FILE.exists():
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)
