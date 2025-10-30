# import os
# import io
# import pickle
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# # Define Google Drive API scope
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# def get_drive_service():
#     """
#     Authenticate with Google Drive API and return a service object.
#     """
#     creds = None
#     token_path = os.path.join(os.getcwd(), "token.pkl")
#     creds_path = os.path.join(os.getcwd(), "credentials.json")

#     # ✅ Load saved credentials if available
#     if os.path.exists(token_path):
#         with open(token_path, 'rb') as token:
#             creds = pickle.load(token)

#     # ✅ Refresh or create new credentials
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             # Make sure credentials.json path exists
#             if not os.path.exists(creds_path):
#                 raise FileNotFoundError(
#                     f"❌ Missing credentials.json file at: {creds_path}\n"
#                     "Please download it from Google Cloud Console → OAuth 2.0 credentials."
#                 )

#             flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
#             creds = flow.run_local_server(port=0)

#         # Save token for next run
#         with open(token_path, 'wb') as token:
#             pickle.dump(creds, token)

#     return build('drive', 'v3', credentials=creds)


# def get_file_download_url(file_id: str) -> str:
#     """
#     Generate a direct Google Drive download URL from file ID.
#     """
#     if not file_id:
#         return None
#     return f"https://drive.google.com/uc?id={file_id}&export=download"


# def download_images_from_folder(folder_id: str, download_dir="downloads"):
#     """
#     Download all images from a Google Drive folder to a local directory.
#     """
#     os.makedirs(download_dir, exist_ok=True)
#     service = get_drive_service()
#     results = service.files().list(
#         q=f"'{folder_id}' in parents and mimeType contains 'image/'",
#         fields="files(id, name)"
#     ).execute()

#     files = results.get('files', [])
#     downloaded_files = []

#     for file in files:
#         request = service.files().get_media(fileId=file['id'])
#         fh = io.FileIO(os.path.join(download_dir, file['name']), 'wb')
#         downloader = MediaIoBaseDownload(fh, request)
#         done = False
#         while not done:
#             _, done = downloader.next_chunk()
#         downloaded_files.append(os.path.join(download_dir, file['name']))

#     return downloaded_files


# if __name__ == "__main__":
#     folder_id = "1a4q84D4bhlxvd8jETtFjXRSfi57sDWKZ"  # Example folder ID
#     print("Downloading from Google Drive...")
#     files = download_images_from_folder(folder_id)
#     print(f"✅ Downloaded {len(files)} files.")

from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def get_drive_service():
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/service_account.json")

    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"❌ Missing service account key at {creds_path}")

    creds = service_account.Credentials.from_service_account_file(
        creds_path,
        scopes=["https://www.googleapis.com/auth/drive"]
    )

    service = build("drive", "v3", credentials=creds)
    return service

    
def get_file_download_url(file_id: str) -> str:
    """Generate a direct download link for a Google Drive file ID."""
    return f"https://drive.google.com/uc?id={file_id}"
