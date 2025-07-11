def login_check(username: str, password: str):
    # Hardcoded credentials
    USERS = {
        "tarun": {"password": "admin123", "role": "admin"},
        "john": {"password": "johnpass", "role": "manager"},
        "worker": {"password": "workerpass", "role": "user"},
    }
    user = USERS.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None
