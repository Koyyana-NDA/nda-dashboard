import json
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from intuitlib.enums import Scopes
from backend.token_store import load_tokens

CLIENT_ID = "ABIM9cvqoskNlO90kyYGBApuXRq0P6rxEJjn3EkoMUSqsWiZ7i"
CLIENT_SECRET = "optlsOoVk4dGZsI5Z8tHPFHC206YNNVeqGi0Ffb7"
REDIRECT_URI = "https://nda-dashboard.onrender.com/callback"
ENVIRONMENT = "production"

ACCOUNTING_SCOPE = Scopes.ACCOUNTING

def get_qbo_client():
    tokens = load_tokens()
    auth_client = AuthClient(
        CLIENT_ID,
        CLIENT_SECRET,
        REDIRECT_URI,
        environment=ENVIRONMENT
    )
    return QuickBooks(
        auth_client=auth_client,
        refresh_token=tokens["refresh_token"],
        company_id=tokens["realm_id"]
    )

def get_auth_client():
    return AuthClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        environment=ENVIRONMENT,
        redirect_uri=REDIRECT_URI
    )
