from django.contrib.contenttypes.models import ContentType
from .models import Clicknums, ClickDetail
from django.utils import timezone
from django.db.models import Sum
import datetime


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        clicknums, created = Clicknums.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 计数加一
        clicknums.click_num += 1
        clicknums.save()
        # 当天阅读数加一
        date = timezone.now().date()
        clicDetail, created = ClickDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        # 计数加一
        clicDetail.click_num += 1
        clicDetail.save()

    return key


def get_seven_days_click_date(content_type):
    today = timezone.now().date()
    click_nums = []
    dates = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        click_details = ClickDetail.objects.filter(content_type=content_type, date=date)
        result = click_details.aggregate(click_num_sum=Sum('click_num'))
        click_nums.append(result['click_num_sum'] or 0)

    return dates, click_nums
