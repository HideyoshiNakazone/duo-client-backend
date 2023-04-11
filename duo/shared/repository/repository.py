from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def get(self, data):
        pass

    @abstractmethod
    def add(self, data):
        pass

    @abstractmethod
    def remove(self, data):
        pass

    @abstractmethod
    def update(self, data):
        pass