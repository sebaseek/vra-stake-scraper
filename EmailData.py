import os
from dotenv import load_dotenv

load_dotenv()


class EmailData:
    def __init__(self):
        self.gmail_user = os.environ.get('gmail_user')
        self.gmail_password = os.environ.get('gmail_password')
        self.sent_from = os.environ.get('gmail_user')
        self.to = [os.environ.get('gmail_to')]
        self.subject = 'VRA STAKING UPDATE'
        self.body = ''
