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


def make_request(endpoint, params):
    """
    Fetch account info from the Supabase API.
    
    :param endpoint: The endpoint dictionary containing the URL and headers
    :param params: Query parameters for the request
    :return: The JSON response from the API
    """    
    raw_url = endpoint.get("url")
    request_url, request_params = replace_placeholders(
        replace_env_vars(raw_url), params
    )

    headers = endpoint.get("headers", {})
    request_headers = replace_env_vars(headers)
    
    response = requests.get(request_url, params=request_params, headers=request_headers)
    
    if response.status_code in (200, 206):
        return response.json()
    else:
        response.raise_for_status()