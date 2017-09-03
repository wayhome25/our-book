from slacker import Slacker

from django.conf import settings


def slack_notify(text=None, channel='#test', username='알림봇', attachments=None):
    token = settings.SLACK_TOKEN
    slack = Slacker(token)
    slack.chat.post_message(text=text, channel=channel, username=username, attachments=attachments)
