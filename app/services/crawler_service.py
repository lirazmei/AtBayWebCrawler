import datetime
import hashlib
from concurrent.futures import ThreadPoolExecutor

from app.models.file_system_dao import AbstractDao
import logging
import requests

status_option = {1: 'Accepeted', 2: 'Runnning', 3: 'Error', 4: 'Complete', 5: 'Not-Found'}


class CrawlerService(object):

    def __init__(self, dao: AbstractDao, max_workers: int):
        self.dao = dao
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger = logging.getLogger()

    def _run_crawler(self, job_id, url):
        self.logger.debug("Enter to _run_crawler in service")
        try:
            self.dao.update_status(job_id, 'Running')
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                self.dao.insert_data(job_id, html_content)
                self.dao.update_status(job_id, 'Complete')
            else:
                self.dao.update_status(job_id, 'Error')
        except Exception as e:
            self.logger.error(str(e), exc_info=True)

    def get_job_id(self, url):
        self.logger.debug("Enter to get_job_id in service")
        md5_hash = hashlib.md5()
        current_time = datetime.datetime.now()
        md5_hash.update(f'{url}{datetime.datetime.timestamp(current_time)*1000}'.encode('utf-8'))
        hashed_url = md5_hash.hexdigest()
        self.logger.debug(f"Hased url {hashed_url} to get_job_id in service")
        return hashed_url

    def get_status(self, job_id):
        self.logger.debug("Enter to get_status in service")
        return self.dao.get_metadata(job_id)

    def handle_url(self, url):
        self.logger.debug("Enter to handle_url in service")
        job_id = self.get_job_id(url)
        self.dao.create_job(job_id, url)
        self.dao.update_status(job_id, 'Accepted')
        self.logger.debug("Finish job creation in service")
        # with self.executor:
        self.executor.submit(self._run_crawler, job_id, url)
        return job_id
