import os
import json
import uuid
import requests
import keyring

def generate(prompt):
    # Load credentials from keyring
    service_name = "my-ai-assistant/google-creds"
    credentials_json = keyring.get_password(service_name, "google_credentials")
    if not credentials_json:
        raise ValueError("Google credentials not found in keyring. Please set them up using the setup script.")

    credentials = json.loads(credentials_json)
    api_key = credentials.get("api_key")
    if not api_key:
        raise ValueError("Missing API key in credentials.")

    # Define API endpoint and parameters
    api_url = "https://vertex-ai.googleapis.com/v1/images:generate"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "prompt": prompt,
        "max_budget": 10  # Example budget limit
    }

    # Call the API
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise ValueError(f"API call failed: {response.text}")

    # Save the image locally
    image_data = response.content
    image_id = str(uuid.uuid4())
    image_path = os.path.abspath(f"./data/images/{image_id}.png")
    with open(image_path, "wb") as f:
        f.write(image_data)

    return image_path