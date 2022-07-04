import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Email:
    def __init__(self):
        try:
            self.api_key = os.environ.get("SENDGRID_API_KEY")
            self.sender = os.environ.get("SENDER_EMAIL")
        except:
            self.api_key = os.environ["SENDGRID_API_KEY"]
            self.sender = os.environ["SENDER_EMAIL"]

    def send(self, subject: str, recipient: str, html_content: str):
        message = Mail(
            from_email=self.sender,
            to_emails=recipient,
            subject=subject,
            html_content=html_content,
        )
        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            # print(response.headers)
        except Exception as e:
            print(e)
