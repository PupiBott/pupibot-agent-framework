import keyring
import json

def setup_google_credentials():
    service_name = "my-ai-assistant/google-creds"
    credential_key = "google_credentials"

    # Prompt user for the path to the credentials file
    credentials_path = input("Enter the path to your Google credentials JSON file: ")

    # Read the credentials file
    try:
        with open(credentials_path, "r") as f:
            credentials_json = f.read()
            json.loads(credentials_json)  # Validate JSON format
    except Exception as e:
        return

    # Store the credentials securely in keyring
    try:
        keyring.set_password(service_name, credential_key, credentials_json)
    except Exception as e:
        return

if __name__ == "__main__":
    setup_google_credentials()