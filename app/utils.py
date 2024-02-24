import logging

logging = logging.getLogger(__name__)


def send_email(to_email, subject, message):
    logging.info(f'################# EMAIL ################# ')
    logging.info(f'Send email {subject} to user {to_email}')
    logging.info(f'Email message content: \n {message} ')


def send_slack_message(api_token, channel, message):
    logging.info(f'################# SLACK ################# ')
    logging.info(f'Send slack message {message} , to channel {channel} - api_token {api_token} ')
