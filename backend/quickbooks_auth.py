from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes


# ❗ Replace these placeholders with real values later
CLIENT_ID = "AB2musrxcDEJTyLEW9rxifJ5GqtDovqgSL1zK5Gwr9g7fgRmPX"
CLIENT_SECRET = "5lzNLHdG82nk8gHq068VJ4TS968oLYa3oQlfAQLl"
REDIRECT_URI = "http://localhost:8000/callback"
ENVIRONMENT = "sandbox"  # or "production"
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"
REALM_ID = "YOUR_REALM_ID"

ACCOUNTING_SCOPE = Scopes.ACCOUNTING

def get_qbo_client():
    auth_client = AuthClient(
        CLIENT_ID,
        CLIENT_SECRET,
        REDIRECT_URI,
        environment=ENVIRONMENT
    )

    client = QuickBooks(
        auth_client=auth_client,
        refresh_token=REFRESH_TOKEN,
        company_id=REALM_ID
    )

    return client

def get_auth_client():
    return AuthClient(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        environment=ENVIRONMENT,
        redirect_uri=REDIRECT_URI
    )
