import requests
from typing import List


class PapercastClient:
    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port

    def add(
        self,
        pipeline: str = "default",
        **kwargs,
    ):

        url = f"http://{self.hostname}:{self.port}/add"
        params = {
            **kwargs,
            "pipeline": pipeline,
        }
        response = requests.post(url, json=params)
        return response

    def pipelines(self):
        url = f"http://{self.hostname}:{self.port}/pipelines"
        response = requests.get(url)
        return response.text

    def _status(self):
        url = f"http://{self.hostname}:{self.port}/status"
        response = requests.get(url)
        return response.text
