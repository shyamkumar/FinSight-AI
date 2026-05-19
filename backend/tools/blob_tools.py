from azure.storage.blob import BlobServiceClient
import os

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

container_name = "financial-reports"

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

container_client = blob_service_client.get_container_client(
    container_name
)


def upload_pdf_to_blob(file_name, file_data):

    blob_client = container_client.get_blob_client(file_name)

    blob_client.upload_blob(
        file_data,
        overwrite=True
    )

    return blob_client.url