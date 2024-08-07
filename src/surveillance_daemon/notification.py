import logging

from mailjet_rest import Client

from services import user_service


class Notification:
    """A class to send notifications to users."""

    def __init__(self, mailjet_api_key: str, mailjet_secret_key: str):
        """Initialize the Notification class."""
        self.to_emails = user_service.get_emails()
        self.api_key = mailjet_api_key
        self.secret_key = mailjet_secret_key
        self.client = Client(auth=(self.api_key, self.secret_key), version="v3.1")
        self.logger = logging.getLogger(__name__)

    def send(self, detected_objects: str):
        object_str = ""
        for obj, conf in detected_objects.items():
            object_str += f"\t* {obj}: {conf}\n\n"

        message = f"Hello,\n\nSome objects were detected by the system:\n\n{object_str}Best\nSmartcam Surveillance System"
        data = {
            "Messages": [
                {
                    "From": {"Email": "gunes314@gmail.com", "Name": "Smartcam Surveillance System"},
                    "To": [{"Email": email} for email in self.to_emails],
                    "Subject": "Smartcam Alert",
                    "TextPart": message,
                }
            ]
        }

        result = self.client.send.create(data=data)
        self.logger.info(f"Sent notification to {self.to_emails}: {result.status_code}")
        return result.status_code
