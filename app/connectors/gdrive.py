import json
import os
from typing import List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.config.settings import (
    GOOGLE_CREDENTIALS,
    GOOGLE_CREDENTIALS_JSON,
    GOOGLE_CREDENTIALS_PATH,
    RAW_DATA_PATH,
)

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
SUPPORTED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
    "text/plain",
}


def _build_credentials():
    if GOOGLE_CREDENTIALS_JSON:
        return service_account.Credentials.from_service_account_info(
            json.loads(GOOGLE_CREDENTIALS_JSON), scopes=SCOPES
        )

    credentials_path = GOOGLE_CREDENTIALS_PATH or GOOGLE_CREDENTIALS
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "Google Drive credentials not found. Set GOOGLE_CREDENTIALS_JSON or provide credentials.json."
        )

    return service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )


def get_drive_service():
    creds = _build_credentials()
    return build("drive", "v3", credentials=creds)


def list_files(folder_id: Optional[str] = None):
    service = get_drive_service()

    query = "trashed = false"
    if folder_id:
        query = f"'{folder_id}' in parents and trashed = false"

    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name, mimeType)",
    ).execute()

    return results.get("files", [])


def download_file(file_id, file_name, destination_dir: str = RAW_DATA_PATH):
    service = get_drive_service()
    os.makedirs(destination_dir, exist_ok=True)

    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(destination_dir, file_name)

    with open(file_path, "wb") as f:
        f.write(request.execute())

    return file_path


class GoogleDriveConnector:
    def fetch_all(self, folder_id: str):
        downloaded_paths: List[str] = []

        for file_info in list_files(folder_id):
            mime_type = file_info.get("mimeType", "")
            if mime_type not in SUPPORTED_MIME_TYPES:
                continue

            downloaded_paths.append(
                download_file(file_info["id"], file_info["name"])
            )

        return downloaded_paths