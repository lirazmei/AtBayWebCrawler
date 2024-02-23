import json
import logging
import os
from .abstract_dao import AbstractDao
from app.conf import STATUS_OPTIONS, DATA_PATH, METADATA_FILEPATH

logger = logging.getLogger(__name__)


class FileSystemDao(AbstractDao):
    def get_metadata(self, job_id: str):
        logger.debug("Enter to get_metadata in FileSystemDao")
        try:
            with open(METADATA_FILEPATH.format(job_id=job_id), 'r') as json_file:
                data_read = json.load(json_file)
            return data_read
        except Exception as e:
            self.logger.error(f'There is no {job_id} in the system. Error is {str(e)} ')
        return {'job_id': job_id, 'status': STATUS_OPTIONS[5]}

    def update_status(self, job_id: str, status: STATUS_OPTIONS):
        logger.debug("Enter to update_status in FileSystemDao")
        with open(METADATA_FILEPATH.format(job_id=job_id), 'r') as json_file:
            data = json.load(json_file)
        data["status"] = status
        with open(METADATA_FILEPATH.format(job_id=job_id), 'w') as json_file:
            json.dump(data, json_file)

    def insert_data(self, job_id: str, data):
        logger.debug("Enter to insert_data in FileSystemDao")
        data_path = DATA_PATH.format(job_id=job_id)
        html_file_path = os.path.realpath(os.path.join(data_path, 'content.html'))
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(data)
        with open(METADATA_FILEPATH.format(job_id=job_id), 'r') as json_file:
            data = json.load(json_file)
        data["html_path"] = html_file_path
        with open(METADATA_FILEPATH.format(job_id=job_id), 'w') as json_file:
            json.dump(data, json_file)

    def create_job(self, job_id, url):
        logger.debug("Enter to create_job in FileSystemDao")
        try:
            data_path = DATA_PATH.format(job_id=job_id)
            if not os.path.exists(data_path):
                os.makedirs(data_path)
                self.logger.debug(f"Folder {data_path} created successfully.")
            else:
                self.logger.warning(f"Folder {data_path} already exists.")
            data_to_write = {
                "job_id": job_id,
                "url": url
            }
            with open(METADATA_FILEPATH.format(job_id=job_id), 'w') as json_file:
                json.dump(data_to_write, json_file)
            self.logger.debug(f"File {METADATA_FILEPATH.format(job_id=job_id)} created successfully.")
        except Exception as e:
            self.logger.error(f'There is no {job_id} in the system. Error is {str(e)} ')
