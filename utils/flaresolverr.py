import requests

class Flaresolverr:
    def __init__(self, endpoint="http://localhost:8191"):
        self.endpoint = endpoint.rstrip("/")

    def get(self, url, proxy=None, max_timeout=60000):
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": max_timeout
        }
        if proxy:
            payload["proxy"] = proxy
        resp = requests.post(f"{self.endpoint}/v1", json=payload)
        resp.raise_for_status()
        return resp.json()["solution"]

    def get_cookies(self, url, proxy=None, max_timeout=60000):
        solution = self.get(url, proxy, max_timeout)
        return solution.get("cookies", [])

    def get_html(self, url, proxy=None, max_timeout=60000):
        solution = self.get(url, proxy, max_timeout)
        return solution.get("response", "") 