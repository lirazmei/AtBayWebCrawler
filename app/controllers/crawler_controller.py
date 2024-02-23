import logging

from flasgger import swag_from
from app.controllers.response_builder import ok, server_error
from os import path
from flask import jsonify, request

logger = logging.getLogger(__name__)


class CrawlerController(object):
    def __init__(self, crawler_service):
        self.crawler_service = crawler_service

    @swag_from(path.join('..', 'swaggers', 'post_crawl_url.yml'))
    def initiate_crawl(self):
        logger.debug("Enter to initiate_crawl in controller")
        data = request.get_json(silent=True)
        try:
            url = data.get('url')
            crawl_id = self.crawler_service.handle_url(url)
            return ok({"crawl_id": crawl_id})
        except Exception as e:
            return server_error({"error": str(e)})

    @swag_from(path.join('..', 'swaggers', 'get_crawl_url.yml'))
    def get_job_status(self, job_id):
        logger.debug("Enter to get_job_status in controller")
        try:
            job_status = self.crawler_service.get_status(job_id)
            job_status_summary = {'job_id': job_id, 'job_status': job_status}
            return ok(job_status_summary)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            return server_error({"error": str(e)})
