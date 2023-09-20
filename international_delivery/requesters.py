import abc
import requests

from logger.tasks import request_logger


class AbstractRequester(abc.ABC):
    @abc.abstractproperty
    def domain(self):
        ...

    @abc.abstractmethod
    def headers(self):
        ...

    def __init__(self) -> None:
        assert self.domain

    @request_logger
    def _get(self, path, params=None):
        assert path

        return requests.get(  # TODO add nonresponding and unsuccessfull response handler
            url=self.domain + path,
            params=params,
            headers=self.headers,
        )
    
    @request_logger
    def _post(self, path, body, params=None):
        assert path
        assert body

        return requests.post(
            url=self.domain + path,
            headers=self.headers,
            data=body,
        )