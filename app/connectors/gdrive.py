from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.config.settings import GOOGLE_CREDENTIALS

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS, scopes=SCOPES
    )

    service = build('drive', 'v3', credentials=creds)
    return service


def list_files():
    service = get_drive_service()

    results = service.files().list(
        pageSize=10,
        fields="files(id, name, mimeType)"
    ).execute()

    files = results.get('files', [])
    return files

import os

def download_file(file_id, file_name):
    service = get_drive_service()

    request = service.files().get_media(fileId=file_id)

    file_path = os.path.join("data/raw", file_name)

    with open(file_path, "wb") as f:
        f.write(request.execute())

    return file_path