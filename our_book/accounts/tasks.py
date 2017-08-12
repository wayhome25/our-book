from config.celery import app
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

@app.task
def send_email_message_notification(mail_subject, mail_content, user_pk):
    recipients = User.objects.get(pk=user_pk)
    send_mail(mail_subject, mail_content, 'wayhome250@gmail.com', [recipients.email])
    return '이메일 발송 완료'

