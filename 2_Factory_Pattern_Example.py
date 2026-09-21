"""
FACTORY METHOD
Not which behaviour I run
It is about which class do I build

"""

# 1. Seperate "what a vector store can do" from  "which one you have"
from abc import ABC, abstractmethod

# Product - What every backend must be able to do
# A product is what is being build
class VectorStore(ABC):

    # Contract - Every every vector store must satisfy
    @abstractmethod
    def query(self, embedding: list[float], top_k: int) -> list:
        # return top_l nearest matches to embedding
        pass

# 2. One class per backend, implementing that contract
class ChromaVectorStore(VectorStore):
    def __init__(self, host: str, port: int) -> None:
        self._collection = f"Connection to Chroma{host} and {port}"

    def query(self, embedding: list[float], top_k: int) -> list:
        print("Logic to get query results from Chroma")
        return ["Chroma1", "Chroma2", "Chroma3"]
    
class QdrantVectorStore(VectorStore):
    def __init__(self, url: str, collection_name: str) -> None:
        self._client = f"Client: {url}"
        self._collection_name = "My COllection"

    def query(self, embedding: list[float], top_k: int) -> list[dict]:
        print("Logic to get query results from Qdrant")
        return ["Qdrant_1", "Qdrant_2", "Qdrant_3"]

# 3. A designated builder for each product, sharing one orchestration method
## A factory method - its job is to construct and return an object.
## Creator - a class that contains the factory method.

# Creator
class VectorStoreFactory(ABC): # Builds vector store and runs queries without knowing which vector store it is

    @abstractmethod
    def create_store(self) -> VectorStore:
        pass

    def run_query(self, embedding: list[float], top_k: int) -> list[dict]:
        store = self.create_store()
        return store.query(embedding, top_k)

# Concrete Creator
class ChromaDBVectorStoreFactory(VectorStoreFactory):
    def create_store(self):
        return ChromaVectorStore(host = "localhost", port=5000)

class QdrantVectorStoreFactory(VectorStoreFactory):
    def create_store(self):
        return QdrantVectorStore(url="http://localhost:8999", collection_name="mycolle")


# Usage
factory = ChromaDBVectorStoreFactory()
results = factory.run_query([3.5], 4)
print("Chroma -> ",results)

# Swap the backend
factory = QdrantVectorStoreFactory()
results = factory.run_query([3.5], 4)
print("Qdrant -> ",results)
