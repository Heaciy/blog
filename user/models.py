from django.db import models
from django.contrib.auth.models import User


class OAuthRelationship(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    node_id = models.CharField(verbose_name='账号ID', max_length=128)
    OAUTH_TYPE_CHOICES = (
        (0, "Github"),
        (1, "Google"),
        (2, "Facebook"),
        (3, "Twitter"),
        (4, "Instagram"),
    )
    oauth_type = models.IntegerField(default=0, verbose_name='账号类型', choices=OAUTH_TYPE_CHOICES)

    def __str__(self):
        return "<OAuthRelationship: %s>" % self.user.username

    class Meta:
        verbose_name = '绑定账号'
        verbose_name_plural = verbose_name


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='用户名', on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name='昵称', max_length=20)

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)

    class Meta:
        verbose_name = '账号昵称'
        verbose_name_plural = verbose_name


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return 'none'


def has_nickname(self):
    return Profile.objects.filter(user=self).exists()


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return '[%s]' % self.username


User.get_nickname = get_nickname  # 动态绑定
User.has_nickname = has_nickname  # 动态绑定
User.get_nickname_or_username = get_nickname_or_username  # 动态绑定
