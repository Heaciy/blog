from django.contrib import admin
from myblog.models import Blog, Category, Tag
from django.contrib.auth.models import User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Tag)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'author', 'get_click_nums', 'category', 'create_time', 'modify_time']

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """对外键进行设置"""
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            kwargs['queryset'] = User.objects.filter(username=request.user.username)
        return super(BlogAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
