from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .base import AbstractBasePlatform
from ...models import Template


class GooglePlatform(AbstractBasePlatform):
    def __init__(self, credential_path, title):
        super().__init__(credential_path, title)
        self.credential_path = credential_path
        self.title = title

    def connection(self):
        """
        Connecting to google Service account.
        """
        creds = service_account.Credentials.from_service_account_file(filename=self.credential_path)
        try:
            service = build('drive', 'v3', credentials=creds)
            return service

        except HttpError as err:
            raise err

    def create_document(self, **kwargs):
        """
        Documents are created using a google service account
        """
        folder_id = kwargs.get('google_folder_id', None)
        print(folder_id)
        file_metadata = {
            'name': self.title,
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id]
        }
        file = self.connection().files().create(body=file_metadata, fields='id').execute()
        document_id = file.get('id')
        self.attach_google_permission(file_id=document_id)
        data = {'url': f'https://docs.google.com/document/d/{document_id}/edit',
                "document_id": document_id
                }
        return data

    def create_from_template(self, template_id, ):
        template = Template.objects.filter(id=template_id).first()
        file_metadata = {'name': self.title}
        if not template:
            raise 'Template does not exist'
        else:
            template_document_id = template.document_id
            google_driver = self.connection().files().copy(fileId=template_document_id,
                                                           body=file_metadata).execute()
            document_copy_id = google_driver.get('id')
            self.attach_google_permission(file_id=document_copy_id)
            data = {'url': f'https://docs.google.com/document/d/{document_copy_id}/edit',
                    "document_id": document_copy_id
                    }
            return data

    def attach_google_permission(self, file_id):
        permissions = {
            'type': 'anyone',
            'role': 'writer'}
        return self.connection().permissions().create(fileId=file_id,
                                                      body=permissions).execute()











