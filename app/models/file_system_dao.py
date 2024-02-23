import logging

from .abstract_dao import AbstractDao
import json
import os

STATUS_OPTIONS = {1: 'Accepted', 2: 'Running', 3: 'Error', 4: 'Complete', 5: 'Not-Found'}

DATA_PATH = os.path.join('..', 'data', '{job_id}')
METADATA_FILEPATH = os.path.join(DATA_PATH, 'metadata.json')


class FileSystemDao(AbstractDao):
    def get_metadata(self, job_id: str):
        try:
            with open(METADATA_FILEPATH.format(job_id=job_id), 'r') as json_file:
                data_read = json.load(json_file)
            return data_read
        except Exception as e:
            self.logger.error(f'There is no {job_id} in the system. Error is {str(e)} ')
        return {'job_id': job_id, 'status': 'Not-Found'}

    def update_status(self, job_id: str, status: STATUS_OPTIONS):
        with open(METADATA_FILEPATH.format(job_id=job_id), 'r') as json_file:
            data = json.load(json_file)
        data["status"] = status
        with open(METADATA_FILEPATH.format(job_id=job_id), 'w') as json_file:
            json.dump(data, json_file)

    def insert_data(self, job_id: str, data):
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
