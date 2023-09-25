import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# Credentials config
PROJECT_ID = os.getenv('project_id')
PRIVATE_KEY_ID = os.getenv('private_key_id')
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0UahaegNKuxku\n7B4Nt6pnEzUdazoFcPFedClxiP4Db7JGkZUc+Im0mcy+yIuMh4IGULK3yN+uAJ93\n82t+obDekQoAqIvPiB+4sZMZybIRppevyifTCYvWMrnDYu8VA2o7aU6vu9haYgj2\nC1oKUSRbRHRYgSDwzNtfvIRSKUeL3xrfw8Ko/qwjrwDz67d4Ps2p0OxD9TfMKFna\nysSFmYQrjmT4vU98MvAPRLW+dw3ugCS85OOLzcKKZSdQrJaKe+4x9ATQd1VgeOk3\npO9CpinPXU56tqC0obra7v+Eq1f9eikpdFBRSrAxFrmfCVp6XPZcV3e0jv7hA5yw\nZTw/KMrFAgMBAAECggEAAWih6BML84mCqNsvYOwOaL+9qn0r9t7rA9HkgP6Q/XXh\n7qs0fwVyDfclolfuvypP2bzHqKfpF3LpzAYa0OJyf0qiyV6HuRdXKBo7C/iHa5vh\nk34A0aVBcmrzCJO9Smy8Z7pq4vSUvCAH8eQkz+/SWOQwBID9wOPY0uamIf4wkOcp\n8kbttuwBRPfXbv/Z9puJ92Dhk1Wnb0zr7NfPXhz2/4X87i1qpLKBh5L9rEZoRgYg\noAL6CdqQnkgm+NgqIulietzBR5wxVmt8poFYLUSCPnLJ2fweFdnFWXz8Fs28R++i\nzNLhoFN/F6AjHzlfiwc5VC2xwzBFHfdePjUO8kOYAQKBgQDg5Nxv1l+OFdvBNjjm\nLAjt7f4v82fb/bPV4u/7d8w84mfwVpRAlA3CF8nLGapb6sdIHIwpuVg7dlR1oY4m\ngMpN6OAtGGP257oR16VBFvXvPciXZRXIsyw8n+mvOCCWz0Ht3BdzhTfIbXELmBr5\nsFscA+0FYVvfozo6dhlrCE8/iwKBgQDNQndT5cMFkUUMUg5WEXWWRmZCNO/5VEbn\nFfyuF6K5Cqg6jPyl2ZIQ7ThLAsJrzIWJjouzaChKp64RL4zyf+7uKXXFiVblKlVO\nYQBW3Vh5FxCQsqTPBYfkmdqGZ6E2WELdEoWjMYMyNAhOWK7+lp+spOd54i74H4tH\ncKU9jZRo7wKBgDn+Smn8mf+F23ljhiC00kioypeK6QltzuYk80WhiuVYbP0pFmng\nw/t9LuhU4f15+ZG66toHlZ0f0n/S/VkodQLKPqTiWUTeVLktJsw2I41iHUwNIST0\nL0Ai7JvmmWDKaXHxA4sim1PwBOq8ephQxe3fhUuR46Mz8FwLAFr9dZIpAoGAELZQ\nsOwMLO/fB1nHAQr63/lragiVYV+TRk1r/WC/RwGvINVJ3NcSJX6rDrBy1AQa+1A3\n36ujXDC643tTpor0EUAe7q53/MCtoWwUcv4irflKx/1Dnfd9UQeV20ukvKADEazo\nZJkrbXL/GiHuXZw19ACZODtKR7mJxY9OZOyaINECgYEAl6kNVlMD2DhLIvo0p/FR\nmJeG9ZEJ0nAPLk6XGePZG+40lpI4roYvyoQyQWM6qbycKDeHv85ZfPKtd/bsGEwU\ni/5bgRIeLxRdz84mnVTEfU/zJ2bp3N7HroDMWCoHO//QTec/HHF2IRHcEGcdQmOW\n6hws2VvCHFfUUv+zZHRElDQ=\n-----END PRIVATE KEY-----\n".replace(r'\n', '\n')
CLIENT_EMAIL = os.getenv('client_email')
CLIENT_ID = os.getenv('client_id')
CLIENT_X509_CERT_URL = os.getenv('client_x509_cert_url')

# spreadsheet id
SPREADSHEET_ID = os.getenv('spreadsheet_id')

# spreadsheet urls
GAMES_SPREADSHEET_URL = os.getenv('games_spreadsheet_url')
STAT_MASS_SPREADSHEET_URL = os.getenv('stat_mass_spreadsheet_url')
STAT_SPORTS_SPREADSHEET_URL = os.getenv('stat_sports_spreadsheet_url')

# credentials as dict
CREDENTIALS = {
    "type": "service_account",
    "project_id": PROJECT_ID,
    "private_key_id": PRIVATE_KEY_ID,
    "private_key": PRIVATE_KEY,
    "client_email": CLIENT_EMAIL,
    "client_id": CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": CLIENT_X509_CERT_URL,
    "universe_domain": "googleapis.com"
}