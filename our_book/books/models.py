from datetime import timedelta, datetime

from django.db.models.aggregates import Sum
from django.utils import timezone
from django.conf import settings
from django.db import models


class Book(models.Model):
    # 도서정보
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    isbn = models.CharField(max_length=50, unique=True)
    isbn13 = models.CharField(max_length=20, unique=True)
    image = models.URLField()
    link = models.URLField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    pubdate = models.CharField(max_length=10)

    # 추가정보
    created_at = models.DateTimeField(auto_now_add=True)
    rent_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    rent_start = models.DateTimeField(blank=True, null=True)
    rent_end= models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

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
    @property
    def check_overdue(self):
        return self.rent_end < timezone.localtime(timezone.now())


class WishBook(models.Model):
    # 도서정보
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    isbn = models.CharField(max_length=50, unique=True)
    isbn13 = models.CharField(max_length=20, unique=True)
    image = models.URLField()
    link = models.URLField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, blank=True)
    pubdate = models.CharField(max_length=10)

    # 추가정보
    created_at = models.DateTimeField(auto_now_add=True)
    wish_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    # 월별 총액
    @classmethod
    def get_total_price(cls, month):
        total_price = cls.objects.filter(created_at__month=month).aggregate(total=Sum('price'))
        return total_price['total']