import requests

class ClientAPI:
    def __init__(self, url_base):
        self.url_base = url_base

    def get_domains(self):
        url = f"{self.url_base}/security/banned-domains"
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()