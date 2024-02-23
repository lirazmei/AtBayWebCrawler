import logging

logging = logging.getLogger(__name__)


def send_email(to_email, subject, message):
    logging.info(f'Send email subject - {subject} to user {to_email}, {message} ')
    # dummy option to send real email
    # msg = MIMEMultipart()
    # msg['From'] = SOURCE_EMAIL
    # msg['To'] = to_email
    # msg['Subject'] = subject
    # body = MIMEText(message)
    # msg.attach(body)
    # with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    #     server.starttls()
    #     server.login(SMTP_USERNAME, SMTP_PASSWORD)
    #     server.sendmail(SOURCE_EMAIL, to_email, msg.as_string())


def send_slack_message(api_token, channel, message):
    logging.info(f'Send slack message {message} , to channel {channel} - api_token {api_token} ')
    # dummy option to send real message to slack
    # client = WebClient(token=api_token)
    # response = client.chat_postMessage(channel=channel, text=message)
    # if response["ok"]:
    #     logging.info(f"Slack message sent to {channel}")
    # else:
    #     logging.error(f"Failed to send Slack message. Error: {response['error']}")
