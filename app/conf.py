import os

SLACK_API_TOKEN = "MOCK_TOKEN"
SOURCE_EMAIL = "your_email@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_email_password"
STATUS_OPTIONS = {1: 'Accepted', 2: 'Runnning', 3: 'Error', 4: 'Complete', 5: 'Not-Found'}
DATA_PATH = os.path.join('..', 'data', '{job_id}')
METADATA_FILEPATH = os.path.join(DATA_PATH, 'metadata.json')
