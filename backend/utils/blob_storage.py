"""Azure Blob Storage utility for file operations."""

from typing import Optional
from datetime import datetime, timedelta, timezone
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
    ContentSettings,
)

## Internal imports
from utils.logging import get_logger
from config import Config

logger = get_logger(__name__)


class AzureBlobStorage:
    """Azure Blob Storage utility class for file operations."""

    def __init__(self):
        """Initialize Azure Blob Storage client using connection string."""
        config = Config.load_configuration()
        self.config = config.storage

        logger.info(f"Connection string: {self.config.connection_string[:30]}...")
        logger.info(f"Account name: {self.config.account_name}")
        logger.info(f"Container name: {self.config.container_name}")

        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.config.connection_string
            )
            logger.info("Successfully created blob service client")

            # Ensure container exists with simple approach
            self._ensure_container_exists(self.config.container_name)

        except Exception as e:
            logger.error(f"Error initializing Azure Blob Storage: {e}")
            raise

    def _ensure_container_exists(self, container_name: str) -> None:
        """Ensure the container exists, create it if it doesn't."""
        try:
            # Try to create the container - if it already exists, this will fail with a specific error
            try:
                self.blob_service_client.create_container(container_name)
                logger.info(f"Container '{container_name}' created successfully")
            except Exception as e:
                # If container already exists, this is fine
                if "ContainerAlreadyExists" in str(e):
                    logger.info(f"Container '{container_name}' already exists")
                else:
                    # If it's another error, re-raise it
                    logger.error(f"Error creating container: {e}")
                    raise
        except Exception as e:
            logger.error(f"Error ensuring container exists: {e}")
            raise

    def upload_file(
        self, file_content: bytes, blob_name: str, content_type: Optional[str] = None
    ) -> str:
        """Upload a file to Azure Blob Storage.

        Args:
            file_content: The file content as bytes
            blob_name: The name to use for the blob
            content_type: The content type of the file

        Returns:
            str: The blob name (object key)
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.config.container_name, blob=blob_name
            )

            content_settings = ContentSettings(content_type=content_type)
            blob_client.upload_blob(
                file_content,
                overwrite=True,
                content_settings=content_settings if content_type else None,
            )

            logger.info(f"File uploaded successfully to blob '{blob_name}'")
            return blob_name
        except Exception as e:
            logger.error(f"Error uploading file to blob storage: {e}")
            raise

    def download_file(self, blob_name: str) -> bytes:
        """Download a file from Azure Blob Storage.

        Args:
            blob_name: The name of the blob to download

        Returns:
            bytes: The file content
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.config.container_name, blob=blob_name
            )

            download = blob_client.download_blob()
            file_content = download.readall()

            logger.info(f"File downloaded successfully from blob '{blob_name}'")
            return file_content
        except Exception as e:
            logger.error(f"Error downloading file from blob storage: {e}")
            raise

    def delete_file(self, blob_name: str) -> None:
        """Delete a file from Azure Blob Storage.

        Args:
            blob_name: The name of the blob to delete
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.config.container_name, blob=blob_name
            )

            blob_client.delete_blob()
            logger.info(f"File deleted successfully from blob '{blob_name}'")
        except Exception as e:
            logger.error(f"Error deleting file from blob storage: {e}")
            raise

    def generate_sas_url(self, blob_name: str, expiry_hours: int = 1) -> str:
        """Generate a SAS URL for a blob with read permissions.

        Args:
            blob_name: The name of the blob
            expiry_hours: Number of hours until the SAS token expires

        Returns:
            str: The SAS URL for the blob
        """
        try:
            # Calculate expiry time (using timezone-aware datetime)
            expiry = datetime.now(timezone.utc) + timedelta(hours=expiry_hours)

            # Generate SAS token
            sas_token = generate_blob_sas(
                account_name=self.config.account_name,
                container_name=self.config.container_name,
                blob_name=blob_name,
                account_key=self.config.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=expiry,
            )

            # Construct the full URL
            sas_url = f"https://{self.config.account_name}.blob.core.windows.net/{self.config.container_name}/{blob_name}?{sas_token}"

            logger.info(
                f"SAS URL generated for blob '{blob_name}', expires in {expiry_hours} hours"
            )
            return sas_url
        except Exception as e:
            logger.error(f"Error generating SAS URL: {e}")
            raise
