from abc import ABC, abstractmethod


class Endpoint(ABC):
    @property
    def name(self):
        return self.__class__.__name__.lower()

    @abstractmethod
    async def generate(self):
        raise NotImplementedError('generate has not been implemented on this endpoint')
