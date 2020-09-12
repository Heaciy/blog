from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from read_statistics.models import ClicknumsExpand, ClickDetail
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.contenttypes.fields import GenericRelation


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(verbose_name='文章类别', unique=True, max_length=20)

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(verbose_name='文章标签', unique=True, max_length=20)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model, ClicknumsExpand):
    """
    博客
    """
    title = models.CharField(verbose_name='标题', max_length=100)
    title_description = models.CharField(verbose_name='描述', max_length=200, default='')
    cover_source = models.ImageField(max_length=100, upload_to='cover/%Y/%m/%d', default='cover/default/unamed.jpg',
                                     verbose_name='封面')
    cover = ImageSpecField(
        source="cover_source",
        processors=[ResizeToFill(700, 220)],
        format='JPEG',
        options={'quality': 100}
    )
    cover_min = ImageSpecField(
        source="cover_source",
        processors=[ResizeToFill(220, 220)],
        format='JPEG',
        options={'quality': 100}
    )
    content = RichTextUploadingField(verbose_name='正文', default='')
    category = models.ForeignKey(Category, verbose_name='文章类别', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    click_details = GenericRelation(ClickDetail)

    def get_url(self):
        return reverse('blog_id', kwargs={'blog_id': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog%d: %s>" % (self.id, self.title)

    class Meta:
        verbose_name = '我的博客'
        verbose_name_plural = verbose_name
