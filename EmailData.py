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
        self.text = ''

    def set_mail_body(self, vra_default_value, vra_number):
        self.body = f'Veracity Value has changed from ${vra_default_value} to ${vra_number}'

    def set_mail_text(self, body):
        self.text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (self.sent_from, ", ".join(self.to), self.subject, body)
