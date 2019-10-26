import datetime
from django.utils import timezone
from django.db.models import Sum
from django.db.models.aggregates import Count
from myblog.models import Tag, Blog
from django.core.cache import cache

def data_for_json():
    tag_list = Tag.objects.annotate(blog_num=Count('blog')).filter(blog_num__gt=0)
    words_json = []
    for tag in tag_list:
        words_json.append({'text': tag.name, 'weight': tag.blog_num, 'link': '/tags/'+tag.name})
    print(words_json)
    return words_json

def get_7_days_hot_days():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(click_details__date__lt=today, click_details__date__gte=date) \
                .annotate(click_num_sum=Sum('click_details__click_num')) \
                .order_by('-click_num_sum')
    return blogs

def get_hot_blogs_from_cache():
    hot_blog_for_7_days = cache.get('hot_blog_for_7_days')
    if hot_blog_for_7_days is None:
        hot_blog_for_7_days = get_7_days_hot_days()
        cache.set('hot_blog_for_7_days', hot_blog_for_7_days, 60)
    return hot_blog_for_7_days[:4]