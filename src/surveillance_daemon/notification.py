class Notification:
    """A class to send notifications to users."""

    def __init__(self, to_email: str):
        self.to_email = to_email

    def send(self, message: str):
        print(message)
