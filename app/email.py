import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Email:
    def __init__(self):
        self.api_key = os.environ.get("SENDGRID_API_KEY")
        self.sender = os.environ.get("SENDER_EMAIL")

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
