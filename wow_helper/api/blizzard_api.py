import requests

from wow_helper import config, utils
from wow_helper.api import Namespace

logger = utils.get_logger(__name__)
BLIZZARD_API = 'https://{0}.api.blizzard.com{1}'

# TODO : MORE WORK SHELVED FOR LATER
class BlizzardAPI:
    def __init__(self):
        self._client_id = config.be_client_id()
        self._client_secret = config.be_client_secret()
        self._access_token = BlizzardAPI._create_access_token(self._client_id, self._client_secret)
        self._session = requests.Session()

    @staticmethod
    def _create_access_token(client_id: str, client_secret: str, region: str = 'us') -> str:
        data = {'grant_type': 'client_credentials'}
        response = requests.post(f'https://{region}.battle.net/oauth/token', data=data, auth=(client_id, client_secret))
        token = response.json()['access_token']
        return token

    def _get_resource(self, resource: str, query_params: dict, region: str = 'us') -> dict:
        url = BLIZZARD_API.format(region, resource)
        response = self._session.get(url, params=query_params)
        return response.json()

    def get_realm_list(self, region: str) -> list:
        query_params = {
            'namespace': f'{Namespace.DYNAMIC.value}-{region}',
            'locale': 'en_US',
            'access_token': self._access_token,
        }

        realms = self._get_resource('/data/wow/realm/index', query_params, region=region)['realms']
        realm_list = [realm['name'] for realm in realms]
        logger.debug(realm_list)
        return realm_list


