import logging
from flask import Flask

logging = logging.getLogger(__name__)
app = Flask(__name__)


def create_routes(app, **controllers):
    crawler_app = controllers['crawler_controller']
    app.add_url_rule('/crawl', endpoint='post_url',
                     view_func=crawler_app.initiate_crawl, methods=['POST'])
    app.add_url_rule('/crawl/<string:crawl_id>', endpoint='fetch_status',
                     view_func=crawler_app.get_job_status, methods=['GET'])
