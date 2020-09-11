from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from myblog.models import Blog, Tag, Category
import markdown
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage
from read_statistics.utils import read_statistics_once_read
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_click_date
from .utils import data_for_json, get_hot_blogs_from_cache


# Create your views here.
class IndexView(View):
    """
    首页
    """

    def get(self, request):
        template = get_template('index.html')
        all_blogs = Blog.objects.all().order_by('-id')
        user = request.user

        hot_blog_for_7_days = get_hot_blogs_from_cache()

        # 使用markdown处理每篇博客
        for blog in all_blogs:
            blog.content = markdown.markdown(blog.content)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blogs, 3, request=request)  # 3为每页展示的博客数目
        all_blogs = p.page(page)

        all_tags = Tag.objects.all().order_by('-id')
        all_categorys = Category.objects.all()
        html = template.render(locals())
        return HttpResponse(html)


class TagDetailView(View):
    """
        标签下的所有博客
        """

    def get(self, request, tag_name):
        template = get_template('tag-detail.html')
        # tag = get_object_or_404(Tag, name=tag_name)
        # 上面一行和下面一行二取一
        tag = Tag.objects.filter(name=tag_name).annotate(blog_num=Count('blog')).first()
        tag_blogs = tag.blog_set.all()  # 注意这里blog_set的用法
        all_tags = Tag.objects.all().order_by('-id')
        all_categorys = Category.objects.all()
        user = request.user

        hot_blog_for_7_days = get_hot_blogs_from_cache()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(tag_blogs, 5, request=request)  # 5为每页展示的博客数目

        tag_blogs = p.page(page)
        html = template.render(locals())
        return HttpResponse(html)


class CategoryDetailView(View):
    """
        分类下的所有博客
        """

    def get(self, request, category_name):
        template = get_template('category-detail.html')
        category = Category.objects.filter(name=category_name).annotate(blog_num=Count('blog')).first()
        category_blogs = category.blog_set.all()  # 注意这里blog_set的用法
        all_tags = Tag.objects.all().order_by('-id')
        all_categorys = Category.objects.all()
        user = request.user

        hot_blog_for_7_days = get_hot_blogs_from_cache()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(category_blogs, 5, request=request)  # 5为每页展示的博客数目

        category_blogs = p.page(page)
        html = template.render(locals())
        return HttpResponse(html)


class BlogDetailView(View):
    """
    博客详情页
    """

    def get(self, request, blog_id):
        template = get_template('blog-detail.html')
        blog = get_object_or_404(Blog, pk=blog_id)
        tags = Tag.objects.all().order_by('-id')
        categorys = Category.objects.all().order_by('-id')
        user = request.user
        hot_blog_for_7_days = get_hot_blogs_from_cache()
        read_cookie_key = read_statistics_once_read(request, blog)
        blog.content = markdown.markdown(blog.content)
        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        id_prev = id_next = int(blog_id)
        blog_id_max = Blog.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        while not has_prev and id_prev >= 1:
            blog_prev = Blog.objects.filter(id=id_prev - 1).first()
            if not blog_prev:
                id_prev -= 1
            else:
                has_prev = True
        while not has_next and id_next <= id_max:
            blog_next = Blog.objects.filter(id=id_next + 1).first()
            if not blog_next:
                id_next += 1
            else:
                has_next = True;

        html = template.render(locals(), request)
        # template.render(),这里的render()的第一个参数必须是要渲染的参数字典，第二个参数是request是为了{% csrf_token %}
        html_responsed = HttpResponse(html)
        html_responsed.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
        return html_responsed


class ArichiveView(View):
    """
    更多信息
    """

    def get(self, request):
        template = get_template('archive.html')
        # 最近一周阅读量统计
        blog_content_type = ContentType.objects.get_for_model(Blog)
        dates, click_nums = get_seven_days_click_date(blog_content_type)

        all_blogs = Blog.objects.all().order_by('-create_time')
        all_tags = Tag.objects.all().order_by('-id')
        user = request.user

        hot_blog_for_7_days = get_hot_blogs_from_cache()

        tag_list = Tag.objects.annotate(blog_num=Count('blog'))
        tags_json = data_for_json()

        all_categorys = Category.objects.all()
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_blogs, 20, request=request)
        all_blogs = p.page(page)
        html = template.render(locals())
        return HttpResponse(html)


def get_faq(request):
    context = {}
    return render(request, 'FAQ.html', context)
