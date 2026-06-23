from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from utils.config import AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_CONTAINER

credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
    credential=credential,
)

container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)


def upload_file(local_file_path: str, blob_name: str) -> str:
    with open(local_file_path, "rb") as file:
        container_client.upload_blob(
            name=blob_name,
            data=file,
            overwrite=True,
        )

    return f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER}/{blob_name}"


def download_blob(blob_name: str) -> bytes:
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client.download_blob().readall()


def list_documents() -> list[str]:
    return [blob.name for blob in container_client.list_blobs()]