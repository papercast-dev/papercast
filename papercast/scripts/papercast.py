import sys
import requests


def call_api(endpoint, params):
    """
    Call the specified API endpoint with the given parameters.

    Args:
        endpoint (str): The name of the API endpoint to call.
        params (dict): A dictionary of parameters to pass to the endpoint.

    Returns:
        dict: A dictionary representing the JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If the API call fails due to a network
            error or invalid response status code.

    The function constructs a URL based on the provided parameters, and sends a POST request
    to the API with JSON-encoded parameters. If the request succeeds and returns a valid JSON
    response, the response dictionary is returned. If the request fails due to a network error
    or an invalid response status code (e.g., 404 Not Found), a `requests.exceptions.RequestException`
    is raised.

    """

    print(f"Calling {endpoint} with parameters {params}.")
    if "hostname" in params:
        base_url = f"http://{params['hostname']}"
        del params["hostname"]
    else:
        base_url = "http://localhost"
    if "port" in params:
        base_url += f":{params['port']}"
        del params["port"]
    else:
        base_url += ":8000"
    print(f"{base_url}/{endpoint}")
    response = requests.post(f"{base_url}/{endpoint}", json=params)
    return response.json()


def parse_arguments():
    """
    Parse the command-line arguments for the API client.

    Returns:
        tuple: A tuple containing the API endpoint name (str) and a dictionary
            of parameters (dict).

    The function reads the command-line arguments. The first argument is assumed to be the
    API endpoint name. The remaining arguments are parsed to construct a dictionary of
    parameters based on the "--key value" syntax. If a key is specified without a value,
    an empty list is added to the dictionary. The function also converts the hyphen-separated
    key names to underscore-separated names.
    """
    if len(sys.argv) < 2:
        print("Please provide an endpoint and optionally parameters.")
        sys.exit(1)

    endpoint = sys.argv[1]
    params = {}

    for arg in sys.argv[2:]:
        if arg.startswith("--"):
            key = arg[2:]
            if key:
                params[key] = []
        elif key in params:  # type: ignore
            params[key].append(arg)  # type: ignore
        else:
            print(f"Unexpected parameter {arg}.")
            sys.exit(1)

    # If the parameter contains only one value, extract it from the list
    for key, value in params.items():
        if len(value) == 1:
            params[key] = value[0]

    params = {k.replace("-", "_"): v for k, v in params.items()}
    return endpoint, params


def main():
    endpoint, params = parse_arguments()
    response = call_api(endpoint, params)
    print(response)


if __name__ == "__main__":
    main()
