from django import template
register = template.Library()
from django.db.models.aggregates import Count
from myblog.models import Tag

@register.simple_tag()
def get_tags():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Tag.objects.annotate(blog_num=Count('blog')).filter(blog_num__gt=0)
