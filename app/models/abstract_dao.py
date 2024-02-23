from abc import ABC, abstractmethod
import logging


class AbstractDao(ABC):

    def __init__(self):
        self.logger = logging.getLogger()

    @abstractmethod
    def get_metadata(self, job_id: str):
        pass

    @abstractmethod
    def update_status(self, job_id: str, status: str):
        pass

    @abstractmethod
    def insert_data(self, job_id: str, data):
        pass

    @abstractmethod
    def create_job(self, job_id, url):
        pass
