"""
Implementation of IFetch
"""

import requests

from Modules.Fetch.IFetch import IFetch


class Fetch(IFetch):
    def __init__(self, version: str):
        self.version = version

    def fetch(self, url: str) -> str | None:
        try:
            user_agent = f'LeBit-James/{self.version}'
            headers = {'User-Agent': user_agent, 'Content-Type': 'application/json; charset=utf-8'}
            result = requests.get(url, headers=headers)

            if result.status_code != 200:
                raise Exception(f"Invalid status code: {result.status_code}")

            return result.text
        except Exception as e:
            print(e)