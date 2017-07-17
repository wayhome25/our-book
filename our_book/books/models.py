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

    # 기본정보
    created_at = models.DateTimeField(auto_now_add=True)