import requests

from wow_helper import config, utils

logger = utils.get_logger(__name__)
WARCRAFT_LOGS_CLIENT_API = 'https://www.warcraftlogs.com/api/v2/client'


class WarcraftLogsAPI:
    def __init__(self):
        self._client_id = config.wl_client_id()
        self._client_secret = config.wl_client_secret()
        self._access_token = WarcraftLogsAPI._create_access_token(self._client_id, self._client_secret)
        self._session = requests.Session()

    @staticmethod
    def _create_access_token(client_id: str, client_secret: str, region: str = 'us') -> str:
        data = {'grant_type': 'client_credentials'}
        response = requests.post(f'https://www.warcraftlogs.com/oauth/token', data=data, auth=(client_id, client_secret))
        token = response.json()['access_token']
        return token

    def _get_resource(self, body: dict) -> dict:
        headers = {
            'Authorization': f'Bearer {self._access_token}'
        }
        response = self._session.get(WARCRAFT_LOGS_CLIENT_API, headers=headers, json={"query": body})
        return response.json()

    def get_character_parses(self, character: str, realm: str, region: str) -> list:
        body = """
                query {
                    characterData {
                        character(name: "Kailavoker", serverSlug: "Area-52", serverRegion: "us") {
                            kazzara: encounterRankings(encounterID: 2688)
                            amalamation: encounterRankings(encounterID: 2687)
                            experiments: encounterRankings(encounterID: 2693)
                            assault: encounterRankings(encounterID: 2682)
                            rashok: encounterRankings(encounterID: 2680)
                            zskarn: encounterRankings(encounterID: 2689)
                            magmorax: encounterRankings(encounterID: 2683)
                            echo: encounterRankings(encounterID: 2684)
                            sark: encounterRankings(encounterID: 2685)
                        }
                    }
                }
                """

        data = self._get_resource(body)
        logger.debug(data)
        return data
