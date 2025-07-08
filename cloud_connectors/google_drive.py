import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from utils.config import CREDENTIALS_FILE, GDRIVE_FOLDER_ID

class GoogleDriveConnector:
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    def __init__(self):
        creds = None
        creds = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, self.SCOPES
        ).run_local_server(port=0)
        self.service = build('drive', 'v3', credentials=creds)

    def fetch_supported_files(self):
        mime_filter = "mimeType contains 'text/' or mimeType='application/pdf' or mimeType='image/png' or mimeType='text/csv'"
        query = f"'{GDRIVE_FOLDER_ID}' in parents and ({mime_filter})"
        res = self.service.files().list(q=query, fields="files(id,name,webViewLink,mimeType)").execute()
        return res.get('files', [])

    def download_file(self, file_meta):
        file_id, name = file_meta['id'], file_meta['name']
        fh = io.FileIO(name, 'wb')
        downloader = MediaIoBaseDownload(fh, self.service.files().get_media(fileId=file_id))
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.close()
        return name
