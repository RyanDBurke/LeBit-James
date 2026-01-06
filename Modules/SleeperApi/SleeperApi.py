from Modules.Fetch.Fetch import Fetch

class SleeperApi:
    def __init__(self, api: Fetch, base_url: str):
        self.api = api
        self.base_url = base_url

    def get(self, endpoint: str) -> str:
        url = f"{self.base_url}{endpoint}"
        return self.api.fetch(url=url)

