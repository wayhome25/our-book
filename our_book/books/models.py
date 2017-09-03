from datetime import timedelta, date

from django.core.mail import send_mail
from django.db.models.aggregates import Sum
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce


class Book(models.Model):
    # 도서정보
    title = models.CharField("도서명", max_length=200)
    author = models.CharField("저자", max_length=100)
    publisher = models.CharField("출판사", max_length=100)
    description = models.CharField("책소개", max_length=300, blank=True)
    isbn = models.CharField("ISBN", max_length=25, unique=True)
    isbn13 = models.CharField("ISBN(13자리)", max_length=13, unique=True)
    image = models.URLField("표지이미지", blank=True)
    link = models.URLField("원본링크", blank=True)
    price = models.PositiveIntegerField("가격")
    discount = models.PositiveIntegerField("할인가격", null=True, blank=True)
    pubdate = models.CharField("출판일", max_length=10, blank=True)

    # 추가정보
    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    rent_info = models.OneToOneField('RentHistory', verbose_name='대출정보', blank=True, null=True, related_name='books')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title

    # 대여 메소드
    def rent_book(self, user):
        rent_start = date.today()
        rent_end = date.today() + timedelta(days=7)
        rent_info = self.renthistory_set.create(user=user, rent_start=rent_start, rent_end=rent_end, return_status=False)
        self.rent_info=rent_info
        self.save()

    # 반납 메소드
    def return_book(self):
        self.rent_info.return_status=True
        self.rent_info.return_date = date.today()
        self.rent_info.save()  # Q : update로 한번에 처리할 수 없을까?
        self.rent_info=None
        self.save()

    # 연체여부 확인
    def check_overdue(self):
        return self.rent_info.rent_end < date.today()


class RentHistory(models.Model):
    # 대여이력
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='대출회원')
    book = models.ForeignKey(Book, verbose_name='대출도서')
    rent_start = models.DateField("대여시작일")
    rent_end = models.DateField("대여종료일")
    return_status = models.BooleanField("반납여부")
    return_date = models.DateField("반납일", blank=True, null=True)
    sent_overdue_email = models.BooleanField("연체알람여부", default=False)

    def __str__(self):
        return "{}-{}".format(self.user, self.book)

    @property
    def check_overdue(self):
        return self.rent_end < date.today()

    def send_return_info_email(self):
        recipients = self.user
        mail_subject = '[반납안내] {}님 내일은 대출하신 도서의 반납일입니다.({})'.format(recipients.nickname, self.book.title)
        mail_content = '대출도서:{} / 반납예정일:{}'.format(self.book.title, self.rent_end)
        send_mail(mail_subject, mail_content, 'wayhome250@gmail.com', [recipients.email])

    def send_overdue_email(self):
        recipients = self.user
        mail_subject = '[연체안내] {}님 대출도서가 연체되었습니다.({})'.format(recipients.nickname, self.book.title)
        mail_content = '대출도서:{} / 반납예정일:{}'.format(self.book.title, self.rent_end)
        send_mail(mail_subject, mail_content, 'wayhome250@gmail.com', [recipients.email])
        self.sent_overdue_email = True
        self.save()

    @classmethod
    def get_due_date_books(cls):
        return cls.objects.filter(rent_end=date.today()+timedelta(days=1))


class WishBook(models.Model):
    # 도서정보
    title = models.CharField("도서명", max_length=100)
    author = models.CharField("저자", max_length=100)
    publisher = models.CharField("출판사", max_length=100)
    description = models.CharField("책소개", max_length=300, blank=True)
    isbn = models.CharField("ISBN", max_length=50, unique=True)
    isbn13 = models.CharField("ISBN(13자리)", max_length=20, unique=True)
    image = models.URLField("표지이미지", blank=True)
    link = models.URLField("원본링크", blank=True)
    price = models.PositiveIntegerField("가격")
    discount = models.PositiveIntegerField("할인가격", null=True, blank=True)
    pubdate = models.CharField("출판일", max_length=10, blank=True)

    # 추가정보
    created_at = models.DateTimeField("생성일시", auto_now_add=True, db_index=True)
    wish_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="구매 신청자", null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    # 월별 총액
    @classmethod
    def get_total_price(cls, year, month):
        total_price = cls.objects.filter(created_at__year=year, created_at__month=month).aggregate(total=Coalesce(Sum('price'), 0))
        return total_price['total']

    def cancel_wish_book(self):
        self.delete()
