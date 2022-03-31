from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def google_connection():
    """
    Connecting to google Serice account.

    """
    creds = service_account.Credentials.from_service_account_file(filename='docs/google_credentials.json')
    try:
        service = build('drive', 'v3', credentials=creds)
        return service

    except HttpError as err:
        raise err


def create_doc(name):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': ['1f-VnpsOFm49aOLo5MKq58BHBrvbg8LuN']
    }
    file = google_connection().files().create(body=file_metadata, fields='id').execute()
    google_id = file.get('id')
    permissions = {
        'type': 'anyone',
        'role': 'writer'}
    google_connection().permissions().create(fileId=google_id, body=permissions).execute()
    data = {'url': f'https://docs.google.com/document/d/{google_id}/edit',
            "google_id": google_id
            }
    return data
