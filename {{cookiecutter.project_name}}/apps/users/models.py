import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


def default_date_expired():
    return datetime.datetime(timezone.now().year + settings.EXPIRE_YEAR,
                             timezone.now().month + settings.EXPIRE_MONTH,
                             timezone.now().day + settings.EXPIRE_DAY,
                             0, 0, 0, 0,
                             tzinfo=timezone.get_current_timezone())


class User(AbstractUser):
    SOURCE_ITEM = [('local', 'local'), ('ldap', 'ldap')]
    AVATAR = 'static/image/avatar/default.jpeg'
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name='主键')
    username = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    realname = models.CharField(max_length=128, verbose_name='姓名')
    nickname = models.CharField(max_length=128, unique=True, verbose_name='昵称')
    email = models.EmailField(max_length=128, unique=True, verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机')
    avatar = models.ImageField(upload_to='static/image/avatar', default=AVATAR, verbose_name='头像')
    introduction = models.CharField(max_length=128, null=True, blank=True, verbose_name='简介')
    source = models.CharField(max_length=32, choices=SOURCE_ITEM, verbose_name='来源')
    date_expired = models.DateTimeField(
        default=default_date_expired(), blank=True, null=True,
        db_index=True, verbose_name='Date expired'
    )
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name='创建时间')
    created_by = models.ForeignKey('self', null=True, related_name='create_user', on_delete=models.CASCADE,
                                   verbose_name='创建者')
    updated_by = models.ForeignKey('self', null=True, related_name='updated_user', on_delete=models.CASCADE,
                                   verbose_name='更新者')

    # first_name = None
    # last_name = None
    # date_joined = None

    # groups = models.ManyToManyField(
    #     'users.UserGroup', related_name='users',
    #     blank=True, verbose_name=_('User group')
    # )

    # 重写该方法
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.username


    @property
    def is_expired(self):
        if self.date_expired and self.date_expired < timezone.now():
            return True
        else:
            return False

    @property
    def is_valid(self):
        if self.is_active and not self.is_expired:
            return True
        return False
