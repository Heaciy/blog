from django.contrib import admin
from myblog.models import Blog, Category, Tag
from django.contrib.auth.models import User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'author', 'get_click_nums', 'category', 'create_time', 'modify_time']
    search_fields = ['title', 'content']

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """对外键进行设置"""
        if not request.user.is_superuser:
            if db_field.name == 'author':
                kwargs['initial'] = request.user.id  # 默认为当前用户
                kwargs['queryset'] = User.objects.filter(username=request.user.username)
        return super(BlogAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_queryset(self, request):
        """如果不是超级管理员则只能看见自己的文章"""
        qs = super(BlogAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(author=request.user)
        return qs
