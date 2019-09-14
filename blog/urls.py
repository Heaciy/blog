"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from myblog.views import IndexView, BlogDetailView, TagDetailView, ArichiveView, CategoryDetailView, get_faq
from user.views import login, logout, register, user_info, login_for_medal, change_nikename_medal, send_verification_code, bind_email, change_password, forgot_password
#为了使media也可访问
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^tags/(?P<tag_name>\w+)$', TagDetailView.as_view(), name='tag_name'),
    url(r'^category/(?P<category_name>\w+)$', CategoryDetailView.as_view(), name='category_name'),
    url(r'^blog/(?P<blog_id>\d+)$', BlogDetailView.as_view(), name='blog_id'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^archive/$', ArichiveView.as_view(), name='archive'),
    url(r'^faq/', get_faq, name='get_faq'),
    url(r'^login/', login, name='login'),
    url(r'^login_for_medal/', login_for_medal, name='login_for_medal'),
    url(r'^logout/', logout, name='logout'),
    url(r'^register/', register, name='register'),
    url(r'^comment/', include('comment.urls')),
    url(r'^user_info/', user_info, name='user_info'),
    url(r'^change_nikename/', change_nikename_medal, name='change_nikename_medal'),
    url('bind_email/', bind_email, name='bind_email'),
    url(r'^send_verification_code/', send_verification_code, name='send_verification_code'),
    url(r'^change_password/', change_password, name='change_password'),
    url(r'^forgot_password/', forgot_password, name='forgot_password'),
    url(r'^search/', include('haystack.urls')),
]
#为了使media也可访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
