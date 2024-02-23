from .abstract_dao import AbstractDao
import json
import os

status_option = {1: 'Accepted', 2: 'Running', 3: 'Error', 4: 'Complete', 5: 'Not-Found'}

DATA_PATH = os.path.join('..', 'data', '{job_id}')
METADATA_FILEPATH = os.path.join(DATA_PATH, 'metadata.json')


class FileSystemDao(AbstractDao):
    def get_status(self, job_id: str):
        with open(METADATA_FILEPATH.format(job_id=job_id), 'r') as json_file:
            data_read = json.load(json_file)
        return data_read['status']

    def update_status(self, job_id: str, status: status_option):
        with open(METADATA_FILEPATH.format(job_id=job_id), 'r') as json_file:
            data = json.load(json_file)
        data["status"] = status
        with open(METADATA_FILEPATH.format(job_id=job_id), 'w') as json_file:
            json.dump(data, json_file)

    def insert_data(self, job_id: str, data):
        data_path = DATA_PATH.format(job_id=job_id)
        with open(os.path.join(data_path, 'content.html'), 'w', encoding='utf-8') as f:
            f.write(data)

    def create_job(self, job_id, url):
        data_path = DATA_PATH.format(job_id=job_id)
        if not os.path.exists(data_path):
            os.makedirs(data_path)
            self.logger.debug(f"Folder '{data_path}' created successfully.")
        else:
            self.logger.warning(f"Folder '{data_path}' already exists.")

        data_to_write = {
            "job_id": job_id,
            "url": url,
            "status": "Accepted"
        }
        with open(METADATA_FILEPATH.format(job_id=job_id), 'w') as json_file:
            json.dump(data_to_write, json_file)