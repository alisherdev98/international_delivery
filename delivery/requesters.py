from conf import CBRDAILY_DOMAIN, CBRDAILY_EXCHANGE_PATH
from international_delivery.requesters import AbstractRequester
from international_delivery.utils import cache_decorator
    

class CBRDailyRequester(AbstractRequester):
    domain = CBRDAILY_DOMAIN
    headers = {}
    
    @cache_decorator('exchange_rate')
    def get_exchange(self):
        response = self._get(
            path=CBRDAILY_EXCHANGE_PATH,
        )
        return response.json()