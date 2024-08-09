import sys
import requests
import json


def call_api(endpoint, params):
    print(f"Calling {endpoint} with parameters {params}.")
    base_url = "http://localhost:8000"
    print(f"{base_url}/{endpoint}")
    if params:
        response = requests.post(f"{base_url}/{endpoint}", json=params)
    else:
        response = requests.get(f"{base_url}/{endpoint}")
    response.raise_for_status()
    return response.json()


def parse_arguments():
    if len(sys.argv) < 2:
        print("Please provide an endpoint and optionally parameters.")
        sys.exit(1)

    endpoint = sys.argv[1]
    params = {}

    key = None
    for arg in sys.argv[2:]:
        if arg.startswith("--"):
            key = arg[2:]
            if key:
                params[key] = []
        elif key in params:
            params[key].append(arg)
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
    print(json.dumps(response))


if __name__ == "__main__":
    main()
