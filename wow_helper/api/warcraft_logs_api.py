import requests
from typing import Union

from wow_helper import config, utils

logger = utils.get_logger(__name__)
WARCRAFT_LOGS_OAUTH_URL = 'https://www.warcraftlogs.com/oauth/token'
WARCRAFT_LOGS_CLIENT_URL = 'https://www.warcraftlogs.com/api/v2/client'

DIFFICULTY = {
    5: 'Mythic',
    4: 'Heroic',
    3: 'Normal',
    2: 'LFR',
    1: 'Timewalking'
}

class WarcraftLogsAPI:
    def __init__(self):
        self._client_id = config.wl_client_id()
        self._client_secret = config.wl_client_secret()
        self._access_token = WarcraftLogsAPI._create_access_token(self._client_id, self._client_secret)
        self._session = requests.Session()

    @staticmethod
    def _create_access_token(client_id: str, client_secret: str, region: str = 'us') -> Union[str, None]:
        data = {'grant_type': 'client_credentials'}
        logger.info(f'POST Request sent to {WARCRAFT_LOGS_OAUTH_URL}')
        response = requests.post(WARCRAFT_LOGS_OAUTH_URL, data=data, auth=(client_id, client_secret))

        if response.status_code != 200:
            logger.error('Warcraft Logs API failed to generate access token.')
            return

        token = response.json()['access_token']
        return token

    def _get_resource(self, body: str) -> dict:
        headers = {
            'Authorization': f'Bearer {self._access_token}'
        }
        logger.info(f'GET Request sent to {WARCRAFT_LOGS_CLIENT_URL}')
        response = self._session.get(WARCRAFT_LOGS_CLIENT_URL, headers=headers, json={"query": body})

        if response.status_code != 200:
            logger.error('Warcraft Logs API is unresponsive.')
            return {}
        return response.json()

    def get_character_parses(self, character: str, realm: str, region: str) -> Union[dict, None]:
        body = """
                query {
                    characterData {
                        character(name: "%s", serverSlug: "%s", serverRegion: "%s") {
                            guilds {
                                name
                            }
                            kazzara_dps: encounterRankings(encounterID: 2688)
                            kazzara_hps: encounterRankings(encounterID: 2688, metric: hps)
                            amalgamation_dps: encounterRankings(encounterID: 2687)
                            amalgamation_hps: encounterRankings(encounterID: 2687, metric: hps)
                            experiments_dps: encounterRankings(encounterID: 2693)
                            experiments_hps: encounterRankings(encounterID: 2693, metric: hps)
                            assault_dps: encounterRankings(encounterID: 2682)
                            assault_hps: encounterRankings(encounterID: 2682, metric: hps)
                            rashok_dps: encounterRankings(encounterID: 2680)
                            rashok_hps: encounterRankings(encounterID: 2680, metric: hps)
                            zskarn_dps: encounterRankings(encounterID: 2689)
                            zskarn_hps: encounterRankings(encounterID: 2689, metric: hps)
                            magmorax_dps: encounterRankings(encounterID: 2683)
                            magmorax_hps: encounterRankings(encounterID: 2683, metric: hps)
                            echo_dps: encounterRankings(encounterID: 2684)
                            echo_hps: encounterRankings(encounterID: 2684, metric: hps)
                            sark_dps: encounterRankings(encounterID: 2685)
                            sark_hps: encounterRankings(encounterID: 2685, metric: hps)
                        }
                    }
                }
                """ % (character, realm, region)

        response = self._get_resource(body).get('data')
        if not response:
            return None
        response = response['characterData']['character']

        parsed_output = {
            'guild': response.pop('guilds')[0]['name'],
        }

        for key in response:
            if parsed_output.get(key[:-4]) is None:
                parsed_output[key[:-4]] = []

            if len(response[key]['ranks']) == 0:
                parsed_output[key[:-4]] += [0.0, 'N/A']
            else:
                parsed_output[key[:-4]] += [round(response[key]['ranks'][0]['rankPercent'], 1), DIFFICULTY[response[key]['difficulty']]]
        return parsed_output

