from abc import ABC, abstractmethod
import logging
status_option = {1: 'Accepeted', 2: 'Runnning', 3: 'Error', 4: 'Complete', 5: 'Not-Found'}


class AbstractDao(ABC):

    def __init__(self):
        self.logger = logging.getLogger()

    @abstractmethod
    def get_status(self, job_id: str):
        pass

    @abstractmethod
    def update_status(self, job_id: str, status: status_option):
        pass

    @abstractmethod
    def insert_data(self, job_id: str, data):
        pass

    @abstractmethod
    def create_job(self, job_id, url):
        pass
