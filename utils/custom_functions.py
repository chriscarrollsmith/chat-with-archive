import logging
import requests
import os
import re
from typing import Dict, Any, Tuple, Union, List

logger = logging.getLogger("uvicorn.error")


def replace_placeholders(url: str, params: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Replace placeholders in the URL with values from params."""
    # Replace placeholders in URL
    placeholders = [match[1:-1] for match in re.findall(r'\{.*?\}', url)]

    for placeholder in placeholders:
        if placeholder in params:
            url = url.replace(f"{{{placeholder}}}", str(params.pop(placeholder)))

    return url, params


def replace_env_vars(data: Union[str, Dict[str, Any], List[Any], Any]) -> Any:
    """Recursively replaces {{ENV_VAR}} placeholders with environment variable values.
    
    Intended for inserting API key or bearer token secrets into the URL, request headers, arguments, etc."""
    if isinstance(data, str):
        return re.sub(r"{{(\w+)}}", lambda match: os.environ.get(match.group(1), match.group(0)), data)
    elif isinstance(data, dict):
        return {key: replace_env_vars(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_env_vars(item) for item in data]
    else:
        return data


def make_request(endpoint: Dict[str, Any], params: Dict[str, Any]) -> List[Any]:
    """
    Fetch account info from the Supabase API.
    
    :param endpoint: The endpoint dictionary containing the URL and headers
    :param params: Query parameters for the request
    :return: The JSON response from the API as a list. If the response is a dictionary, it will be wrapped in a list
    """    

    raw_url: Any = endpoint.get("url")
    if not (raw_url and isinstance(raw_url, str)):
        raise ValueError("URL missing from tool schema")

    url_with_env_vars: Union[str, Dict[str, Any], List[Any], Any] = replace_env_vars(raw_url)
    if not (url_with_env_vars and isinstance(url_with_env_vars, str)):
        raise ValueError("Tool schema URL must be a string")

    request_url, request_params = replace_placeholders(url_with_env_vars, params)

    headers: Any = endpoint.get("headers", {})
    if not (headers and isinstance(headers, dict)):
        raise ValueError("Tool schema headers must be a dictionary")

    request_headers: Any = replace_env_vars(headers)
    if not (request_headers and isinstance(request_headers, dict)):
        raise ValueError("Tool schema headers must be a dictionary")

    # Helper function to prepend "eq." to the missing filter in params
    def fix_missing_filter_in_params(d: Any, missing_filter: str):
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, str) and v == missing_filter:
                    d[k] = f"eq.{v}"
                else:
                    fix_missing_filter_in_params(v, missing_filter)
        elif isinstance(d, list):
            for i, val in enumerate(d):
                if isinstance(val, str) and val == missing_filter:
                    d[i] = f"eq.{val}"
                else:
                    fix_missing_filter_in_params(val, missing_filter)

    response = requests.get(
        request_url, 
        params=request_params, 
        headers=request_headers
    )

    if response.status_code in (200, 206):
        data = response.json()
        return [data] if isinstance(data, dict) else data
    else:
        # Attempt to parse a detailed error from the response
        try:
            error_detail = response.json()
            error_message = f"HTTP {response.status_code} Error: {response.reason}. Details: {error_detail}"
        except:
            error_message = f"HTTP {response.status_code} Error: {response.reason}"

        # Check for "failed to parse filter"
        if "failed to parse filter" in error_message:
            error_message += " Did you remember to use PostgREST operators (e.g., eq, neq, gt, gte, lt, lte, like, ilike) for filtering?"

            # Attempt to extract what is inside the parentheses: "failed to parse filter ()"
            match = re.search(r"failed to parse filter \(([^)]*)\)", error_message)
            if match:
                missing_filter = match.group(1)  # the string inside the parentheses

                # Prepend "eq." to the missing filter anywhere it appears in params
                fix_missing_filter_in_params(params, missing_filter)

                # Now rebuild URL and request params because placeholders may have changed
                request_url, request_params = replace_placeholders(url_with_env_vars, params)

                # Retry the request
                response = requests.get(
                    request_url,
                    params=request_params,
                    headers=request_headers
                )
                
                if response.status_code in (200, 206):
                    data = response.json()
                    return [data] if isinstance(data, dict) else data
                else:
                    # If the second attempt also failed, try to parse the new error
                    try:
                        error_detail = response.json()
                        error_message = f"HTTP {response.status_code} Error: {response.reason}. Details: {error_detail}"
                    except:
                        error_message = f"HTTP {response.status_code} Error: {response.reason}"
                    
                    if "timeout" in error_message:
                        error_message += " You may have run a slow query. Try to optimize your query or break it into multiple steps."
                    
                    logger.error(error_message)
                    return error_message  # Return the error message if retry failed too
        
        # If "failed to parse filter" did not appear or the retry logic did not apply, handle timeouts
        if "timeout" in error_message:
            error_message += " You may have run a slow query. Try to optimize your query or break it into multiple steps."

        logger.error(error_message)
        raise requests.exceptions.HTTPError(error_message, response=response)