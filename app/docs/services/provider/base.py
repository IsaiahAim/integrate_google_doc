from abc import ABC, abstractmethod


class AbstractBasePlatform(ABC):
    def __init__(self, credential_path:str, title):
        self.credentials_path = credential_path
        self.title = title

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def create_document(self, **kwargs):
        pass

    @abstractmethod
    def create_from_template(self, **kwargs):
        pass



