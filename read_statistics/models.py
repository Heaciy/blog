from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


class Clicknums(models.Model):
    click_num = models.IntegerField(verbose_name='阅读量', default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读量'
        verbose_name_plural = verbose_name


class ClicknumsExpand():
    def get_click_nums(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            clicknums = Clicknums.objects.get(content_type=ct, object_id=self.pk)
            return clicknums.click_num
        except exceptions.ObjectDoesNotExist:
            return 0


class ClickDetail(models.Model):
    date = models.DateField(default=timezone.now)
    click_num = models.IntegerField(verbose_name='阅读量', default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读量(详细)'
        verbose_name_plural = verbose_name
