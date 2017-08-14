from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from config.celery import app
from books.models import RentHistory


User = get_user_model()

@app.task
def send_email_message_notification(mail_subject, mail_content, user_pk):
    recipients = User.objects.get(pk=user_pk)
    send_mail(mail_subject, mail_content, 'wayhome250@gmail.com', [recipients.email])
    return '이메일 발송 완료'


@app.task
def send_email_return_date_notification():
    due_date_books = RentHistory.get_due_date_books()
    for due_date_book in due_date_books:
        due_date_book.send_return_info_email()
    return '반납일 안내 이메일 발송 완료 ({}개)'.format(len(due_date_books))


@app.task
def send_email_overdue_notification():
    not_returned_books = RentHistory.objects.filter(return_status=False)
    overdue_books = [book for book in not_returned_books if book.check_overdue and not book.sent_overdue_email]
    for overdue_book in overdue_books:
        overdue_book.send_overdue_email()
    return '연체안내 이메일 발송 완료 ({}개)'.format(len(overdue_books))
