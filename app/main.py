import os
import sys
import logging

from flasgger import Swagger, swag_from
from flask import Flask

from routes import create_routes
from controllers.response_builder import ok
from models.file_system_dao import FileSystemDao
from controllers.crawler_controller import CrawlerController
from services.crawler_service import CrawlerService

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/healthcheck')
@swag_from(os.path.join('', 'swaggers', 'healthcheck.yml'))
def healthcheck():
    return ok({"message": "OK"})


IS_DEBUG = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        IS_DEBUG = True


def init_logger():
    log_level = logging.DEBUG if IS_DEBUG else logging.INFO
    root = logging.getLogger()
    root.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == '__main__':
    init_logger()
    swagger = Swagger(app)
    fs_dao = FileSystemDao()
    crawler_service = CrawlerService(fs_dao, max_workers=10)
    create_routes(app, crawler_controller=CrawlerController(crawler_service))
    app.run(debug=IS_DEBUG, port=8000)
