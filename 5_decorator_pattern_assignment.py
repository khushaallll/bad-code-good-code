from abc import ABC, abstractmethod

# component - main class and decorators implement it

class StorageClient(ABC):
    
    @abstractmethod
    def upload(self, data: bytes, key: str) -> bool:
        ...

# concrete class
class Uploader(StorageClient):
    def __init__(self, connection: str):
        self._connection = connection
        
    def upload(self, data: bytes, key: str) -> bool:
        print(f"Connection opened to: {self._connection}")
        print("[modified_data] uploaded successfully")
        return True

# base decorator
class UploaderDecorator(StorageClient):
    def __init__(self, wrapped: StorageClient):
        self._wrapped = wrapped
    
    def upload(self, data: bytes, key: str) -> bool:
        return self._wrapped.upload(data, key)

# concrete decorator 1 - compression
class CompressionDecorator(UploaderDecorator):
    def __init__(self, wrapped: StorageClient, compression_rate: int = 2):
        super().__init__(wrapped)
        self._compression_rate = compression_rate
        
    def compress_data(self, data) -> bytes:
        compressed_data = data # lets just say that we compressed
        return compressed_data 
        
    def upload(self, data: bytes, key: str) -> bool:
        print(f"[compress] data by {self._compression_rate}")
        modified_data = self.compress_data(data)
        return self._wrapped.upload(modified_data, key)

# concrete decorator 2 - encryprion
class EncryptionDecorator(UploaderDecorator):
    
    def encrypt_data(self, data: bytes) -> bytes:
        encrypted_data = data # lets just say we encrypted data
        return encrypted_data
    
    def upload(self, data: bytes, key: str) -> bool:
        print(f"[encrypt] data using key: {key}")
        modified_data = self.encrypt_data(data)
        return self._wrapped.upload(modified_data, key)

upload_obj = EncryptionDecorator(CompressionDecorator(Uploader('https://awsblob.aws')))
resp = upload_obj.upload(b"Python Exercises.", "uzui")
print(resp)