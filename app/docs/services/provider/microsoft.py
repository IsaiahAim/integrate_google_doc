from .base import AbstractBasePlatform


class MicrosoftPlatform(AbstractBasePlatform):
    def __init__(self, title, credentials_path):
        super().__init__(title, credentials_path)
        self.title = title
        self.credentials_path = credentials_path

    def connection(self):
        pass

    def create_document(self):
        pass
