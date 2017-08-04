from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from books.models import Book, RentHistory

class MyUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email,
            nickname=nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(
        '닉네임',
        max_length=10,
        blank=False,
        unique=True,
    )
    TEAM_CHOICES = (
        ('개발', '개발팀'),
        ('경영지원', '경영지원팀'),
        ('디자인', '디자인팀'),
        ('영업', '영업팀'),
        ('운영', '운영팀'),
        ('재무', '재무팀'),
        ('대표', 'CEO'),
        ('기타', '기타'),
    )
    team = models.CharField(
        '부서',
        max_length=10,
        choices=TEAM_CHOICES,
        default='개발'
    )
    avatar = ProcessedImageField(
        verbose_name='프로필 사진',
        help_text='선택사항',
        upload_to='accounts/avatar/',
        processors=[ResizeToFill(150, 150)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
    )
    bio = models.CharField('소개', max_length=200, blank=True)
    birth_date = models.DateField('생일', null=True, blank=True)
    date_joined = models.DateTimeField('가입일', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        # Send an email to this User
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_rent_books(self):
        return Book.objects.filter(rent_info__user=self).order_by('rent_info__rent_end')

    def get_rent_history(self):
        return RentHistory.objects.filter(user=self)
