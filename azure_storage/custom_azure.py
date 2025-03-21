from storages.backends.azure_storage import AzureStorage
import os

class AzureMediaStorage(AzureStorage):
    account_name = os.getenv('AZURE_BLOB_STORAGE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_BLOB_STORAGE_ACCOUNT_KEY')
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = os.getenv('AZURE_BLOB_STORAGE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_BLOB_STORAGE_ACCOUNT_KEY')
    azure_container = 'static'
    expiration_secs = None