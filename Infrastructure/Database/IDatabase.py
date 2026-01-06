from abc import ABC, abstractmethod


class IDatabase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def query(self, sql: str):
        pass

    @abstractmethod
    def upsert(self, sql: str):
        pass

    @abstractmethod
    def close(self):
        pass