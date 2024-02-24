import datetime
import hashlib

import logging
import requests

from concurrent.futures import ThreadPoolExecutor

from app.conf import SLACK_API_TOKEN
from app.utils import send_email, send_slack_message
from app.models.file_system_dao import AbstractDao
from app.conf import STATUS_OPTIONS


class CrawlerService(object):

    def __init__(self, dao: AbstractDao, max_workers: int):
        self.dao = dao
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger = logging.getLogger()

    def process_complete_notify_user(self, crawl_id, url, communication_details):
        self.logger.debug("Enter to process_complete_notify_user in service")
        message = f"Crawl completed successfully for url {url}! - relevant id {crawl_id} "

        if 'email_address' in communication_details.keys():
            email = communication_details['email_address']
            email_subject = f"Crawl {crawl_id} Completed"
            email_message = f"Hello user,\n\n{message}\n\nRegards,\nYour Web Crawler"
            send_email(email, email_subject, email_message)
            self.logger.debug(f"sent email to {email} on crawl {crawl_id}")
        if 'user_name' in communication_details.keys():
            slack_user = communication_details['user_name']
            slack_user_message = f"Hello {slack_user}, {message}"
            send_slack_message(SLACK_API_TOKEN, slack_user, slack_user_message)
            self.logger.debug(
                f"sent notification to slack user {slack_user} on crawl {crawl_id}")
        if 'channel_name' in communication_details.keys():
            slack_channel = communication_details['channel_name']
            slack_channel_message = f"{message}"
            send_slack_message(SLACK_API_TOKEN, slack_channel, slack_channel_message)
            self.logger.debug(
                f"sent notification to slack channel {slack_channel} on crawl {crawl_id}")

    def _run_crawler(self, job_id, url, communication_details):
        self.logger.debug("Enter to _run_crawler in service")
        try:
            self.dao.update_status(job_id, STATUS_OPTIONS[2])
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                self.dao.insert_data(job_id, html_content)
                self.dao.update_status(job_id, STATUS_OPTIONS[4])
                if communication_details != {}:
                    self.process_complete_notify_user(job_id, url, communication_details)
            else:
                self.dao.update_status(job_id, STATUS_OPTIONS[3])
        except Exception as e:
            self.logger.error(str(e), exc_info=True)

    def get_job_id(self, url):
        self.logger.debug("Enter to get_job_id in service")
        md5_hash = hashlib.md5()
        current_time = datetime.datetime.now()
        md5_hash.update(f'{url}{datetime.datetime.timestamp(current_time) * 1000}'.encode('utf-8'))
        hashed_url = md5_hash.hexdigest()
        self.logger.debug(f"Hashed url {hashed_url} to get_job_id in service")
        return hashed_url

    def get_status(self, job_id):
        self.logger.debug("Enter to get_status in service")
        return self.dao.get_metadata(job_id)

    def handle_url(self, url, communication_details):
        self.logger.debug("Enter to handle_url in service")
        job_id = self.get_job_id(url)
        self.dao.create_job(job_id, url)
        self.dao.update_status(job_id, STATUS_OPTIONS[1])
        self.logger.debug("Finish job creation in service")
        self.executor.submit(self._run_crawler, job_id, url, communication_details)
        return job_id
