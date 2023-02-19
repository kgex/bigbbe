# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from dotenv import load_dotenv

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# load_dotenv(os.path.join(BASE_DIR, ".env"))


# class Email:
#     def __init__(self):
#         try:
#             self.api_key = os.environ.get("SENDGRID_API_KEY")
#             self.sender = os.environ.get("SENDER_EMAIL")
#         except:
#             self.api_key = os.environ["SENDGRID_API_KEY"]
#             self.sender = os.environ["SENDER_EMAIL"]

#     def send(self, subject: str, to: str, html_content: str):
#         message = Mail(
#             from_email=self.sender,
#             to_emails=to,
#             subject=subject,
#             html_content=html_content,
#         )
#         try:
#             sg = SendGridAPIClient(self.api_key)
#             response = sg.send(message)
#             print(response.status_code)
#             print(response.body)
#             # print(response.headers)
#         except Exception as e:
#             print(e)

from mailjet_rest import Client
import os


class Email:
    def __init__(self):
        try:
            self.api_key = os.environ.get("MAILJET_API_KEY")
            self.api_secret = os.environ.get("MAILJET_API_SECRET")
        except:
            self.api_key = os.environ["MAILJET_API_KEY"]
            self.api_secret = os.environ["MAILJET_API_SECRET"]

    def send(self, to, subject, html_content):
        mailjet = Client(auth=(self.api_key, self.api_secret), version="v3.1")
        data = {
            "Messages": [
                {
                    "From": {"Email": "tkksctwo@gmail.com", "Name": "KGX"},
                    "To": [
                        {
                            "Email": to,
                        }
                    ],
                    "Subject": subject,
                    "HTMLPart": html_content,
                    "CustomID": "AppGettingStartedTest",
                }
            ]
        }
        result = mailjet.send.create(data=data)
        return result
