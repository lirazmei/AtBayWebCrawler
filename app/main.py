import os
import sys
import logging
import argparse

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


def parser_initialization():
    parser = argparse.ArgumentParser(description='Argument Parser with Debug and Max Workers Flags')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--max-workers', type=int, default=1,
                        help='Specify the maximum number of workers (default: 1)')
    args = parser.parse_args()
    if args.debug:
        logger.info("Debug mode is enabled")
    logger.info(f"Max workers is {args.max_workers}")
    return args


if __name__ == '__main__':
    init_logger()
    logger = logging.getLogger(__name__)
    app_args = parser_initialization()
    swagger = Swagger(app)
    fs_dao = FileSystemDao()
    crawler_service = CrawlerService(fs_dao, max_workers=app_args.max_workers)
    create_routes(app, crawler_controller=CrawlerController(crawler_service))
    app.run(debug=app_args.debug, port=8000)
