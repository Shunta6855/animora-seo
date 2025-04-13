# ライブラリのインポート
from google_auth_oauthlib.flow import InstalledAppFlow

# Use client_secrets.json to authenticate the user
flow = InstalledAppFlow.from_client_secrets_file(
    "config/client_secret.json",
    scopes=["https://www.googleapis.com/auth/adwords"],
)

# Run the flow to get the credentials
credentials = flow.run_flow()

# Print the refresh token
print("Refresh Token:", credentials.refresh_token)