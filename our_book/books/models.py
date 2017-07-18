from datetime import timedelta, datetime

from django.db.models.aggregates import Sum
from django.utils import timezone
from django.conf import settings
from django.db import models


class Book(models.Model):
    # 도서정보
    title = models.CharField("도서명", max_length=100)
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
    created_at = models.DateTimeField("생성일", auto_now_add=True, db_index=True)  # Q: 왜 db_index 옵션이 필요할까?  without indexes it needs to scan over all rows to figure out the order.
    rent_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="대출회원", blank=True, null=True)
    rent_start = models.DateTimeField("대여 시작일", blank=True, null=True)
    rent_end= models.DateTimeField("대여 종료일", blank=True, null=True)

    class Meta:
        ordering = ['-created_at']  # note 생성일자 최신순으로 정렬

    # 대여 메소드
    def rent_book(self, user):
        self.rent_user = user
        self.rent_start = timezone.localtime(timezone.now())
        self.rent_end = timezone.localtime(timezone.now()) + timedelta(days=7)
        # datetime 객체 대신 time-zone-aware datetime 객체 사용
        # 참고 : https://8percent.github.io/2017-05-31/django-timezone-problem/
        self.save()

    # 반납 메소드
    def return_book(self):
        self.rent_user = None
        self.rent_start = None
        self.rent_end = None
        self.save()

    # 연체여부 확인
    def check_overdue(self):
        return self.rent_end < timezone.localtime(timezone.now())


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
    created_at = models.DateTimeField("생성일", auto_now_add=True, db_index=True)
    wish_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="구매 신청자", null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    # 월별 총액
    @classmethod
    def get_total_price(cls, month):
        total_price = cls.objects.filter(created_at__month=month).aggregate(total=Sum('price'))
        return total_price['total']
