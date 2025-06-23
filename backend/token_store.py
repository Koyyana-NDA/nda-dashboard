import json
from pathlib import Path

TOKEN_FILE = Path("backend/tokens.json")

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
