import requests
import json
import os
import re

def replace_placeholders(url, params):
    """Replace placeholders in the URL with values from params."""
    # Replace placeholders in URL
    placeholders = [match[1:-1] for match in re.findall(r'\{.*?\}', url)]

    for placeholder in placeholders:
        if placeholder in params:
            url = url.replace(f"{{{placeholder}}}", str(params.pop(placeholder)))

    return url, params


def get_response(url, headers={}, params={}):
    """
    Fetch account info from the Supabase API.
    
    :param url: The full URL of the account info endpoint
    :param params: Additional parameters for the request
    :return: The JSON response from the API
    """
    url, params = replace_placeholders(url, params)
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code in (200, 206):
        return response.json()
    else:
        response.raise_for_status()


def load_json(file_path):
    """
    Load parameters from a JSON file.
    
    :param file_path: Path to the JSON file
    :return: Dictionary of parameters
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def replace_env_vars(data):
    """Recursively replaces {{ENV_VAR}} placeholders with environment variable values."""
    if isinstance(data, str):
        return re.sub(r"{{(\w+)}}", lambda match: os.environ.get(match.group(1), match.group(0)), data)
    elif isinstance(data, dict):
        return {key: replace_env_vars(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_env_vars(item) for item in data]
    else:
        return data


if __name__ == "__main__":
    print("Loading API parameters...")
    from dotenv import load_dotenv

    load_dotenv()

    # Load all files in the endpoints folder and use extend to add them to the endpoints list
    endpoints = []
    for file in os.listdir("endpoints"):
        try:
            endpoints.extend(load_json(f"endpoints/{file}"))
        except Exception as e:
            print(f"Warning: Failed to load {file}. Error: {e}")

    if not endpoints:
        print("Usage: Populate JSON files in the endpoints folder with the API endpoints you want to call.")
        exit(1)


    calls = load_json("calls.json")
    if not calls:
        print("Usage: Populate calls.json with the API calls you want to make.")
        exit(1)
    for call in calls:
        assert isinstance(call, dict), f"Invalid call format: {call}"
        # If there's a key named "action", rename it to "name"
        if "action" in call:
            call["name"] = call.pop("action")
        # If there's a key named "action_input", rename it to "parameters"
        if "action_input" in call:
            call["parameters"] = call.pop("action_input")

    # Replace environment variables in all endpoints
    endpoints = replace_env_vars(endpoints)
    for endpoint in endpoints:
        assert isinstance(endpoint, dict)

    params = {}
    for call in calls:
        endpoint_name = call.get("name")
        endpoint = next((item for item in endpoints if item["name"] == endpoint_name), None)
        if endpoint:
            url = endpoint.get("url")
            headers = endpoint.get("headers", {})
            params = call.get("parameters")
        else:
            print(f"Warning: Endpoint {endpoint_name} not found")
            continue

        try:
            response = get_response(url, headers, params)
            print("Dumping response to output.json")
            with open(f"output.json", "w") as f:
                json.dump(response, f)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")