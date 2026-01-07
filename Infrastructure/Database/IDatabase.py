from abc import ABC, abstractmethod


class IDatabase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self, sql: str, params: tuple = None, obj: object = None):
        pass