import requests

from app.dashboard.config.settings import DashboardSettings


class AnzenApiClient:
    def __init__(self, url=None, timeout=60):
        self.url = url or DashboardSettings.anzen_external_url
        self.timeout = timeout

    def analizar_repo_github(self, repo_url):
        response = requests.post(
            self.url,
            files={"repo_url": (None, repo_url)},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
