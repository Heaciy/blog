import string
import random
import time
import json
from urllib.request import urlopen
from urllib.parse import urlencode, parse_qs
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm, \
    BindGithubForm
from .models import Profile, OAuthRelationship


def login_by_github(request):
    code = request.GET['code']
    state = request.GET['state']
    if state != settings.GITHUB_STATE:
        raise Exception("state error")
    # 获取Access_token
    params = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.GITHUB_REDIRECT_URL,
        'state': state,
    }
    response = urlopen('https://github.com/login/oauth/access_token?' + urlencode(params))
    data = response.read().decode('utf8')
    access_token = parse_qs(data)['access_token'][0]
    response = urlopen('https://api.github.com/user?access_token=' + access_token)
    data = response.read().decode('utf8')
    node_id = json.loads(data)['node_id']
    github_login = json.loads(data)['login']
    # 获取node_id是否有关联用户
    if OAuthRelationship.objects.filter(node_id=node_id, oauth_type=0).exists():
        relationship = OAuthRelationship.objects.get(node_id=node_id, oauth_type=0)
        auth.login(request, relationship.user)
        return redirect(reverse('index'))
    else:
        request.session['node_id'] = node_id
        request.session['github_login'] = github_login
        return redirect(reverse('bind_github'))


def bind_github(request):
    if request.method == 'POST':
        bind_github_form = BindGithubForm(request.POST)
        if bind_github_form.is_valid():
            user = bind_github_form.cleaned_data['user']
            node_id = request.session.pop('node_id')
            # 记录关系
            relationship = OAuthRelationship()
            relationship.user = user
            relationship.node_id = node_id
            relationship.oauth_type = 0
            relationship.save()
            # 登陆
            auth.login(request, user)
            return redirect(reverse('index'))
    else:
        bind_github_form = BindGithubForm()

    Forgotpasswordform = ForgotPasswordForm()
    context = {}
    context['bind_github_form'] = bind_github_form
    context['Forgotpasswordform'] = Forgotpasswordform
    return render(request, 'bind_github.html', context)


def create_user_by_github(request):
    # 创建用户
    username = request.session.pop('github_login')
    # username = int(time.time())
    password = username + '@heyis.me'
    # password = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    user = User.objects.create_user(username, '', password)
    # 创建昵称
    profile = Profile()
    profile.user = user
    profile.nickname = username
    profile.save()
    # 记录关系
    node_id = request.session.pop('node_id')
    relationship = OAuthRelationship()
    relationship.user = user
    relationship.node_id = node_id
    relationship.oauth_type = 0
    relationship.save()
    # 登陆
    auth.login(request, user)
    return redirect(reverse('index'))


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = LoginForm()

    Forgotpasswordform = ForgotPasswordForm()
    context = {}
    context['login_form'] = login_form
    context['Forgotpasswordform'] = Forgotpasswordform
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 删除session
            del request.session['register_code']
            # 登陆用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('index')))


def user_info(request):
    context = {}
    Nicknameform = ChangeNicknameForm()
    Bindemailform = BindEmailForm()
    Changepasswordform = ChangePasswordForm()
    context['Nicknameform'] = Nicknameform
    context['Bindemailform'] = Bindemailform
    context['Changepasswordform'] = Changepasswordform
    return render(request, 'user_info.html', context)


def change_nikename_medal(request):
    data = {}
    Nicknameform = ChangeNicknameForm(request.POST, user=request.user)
    if Nicknameform.is_valid():
        nickname_new = Nicknameform.cleaned_data['nickname_new']
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.nickname = nickname_new
        profile.save()
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now

            # 发送邮件
            if send_for == 'register_code':
                message = '注册验证'
            elif send_for == 'bind_email_code':
                message = '绑定邮箱'
            else:
                message = '忘记密码'
            send_mail(
                message,
                '验证码：%s，有效期为30分钟' % code,
                'Heaciy' + ' ' + '<' + settings.EMAIL_HOST_USER + '>',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def bind_email(request):
    data = {}
    form = BindEmailForm(request.POST, request=request)
    if form.is_valid():
        email = form.cleaned_data['email']
        request.user.email = email
        request.user.save()
        # 删除session
        del request.session['bind_email_code']
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())[0][0]
    return JsonResponse(data)


def change_password(request):
    data = {}
    Changepasswordform = ChangePasswordForm(request.POST, user=request.user)
    if Changepasswordform.is_valid():
        user = request.user
        old_password = Changepasswordform.cleaned_data['old_password']
        new_password = Changepasswordform.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()
        auth.logout(request)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
        data['message'] = list(Changepasswordform.errors.values())[0][0]
    return JsonResponse(data)


def forgot_password(request):
    data = {}
    Forgotpasswordform = ForgotPasswordForm(request.POST, request=request)
    if Forgotpasswordform.is_valid():
        email = Forgotpasswordform.cleaned_data['email']
        new_password = Forgotpasswordform.cleaned_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        # 清除session
        del request.session['forgot_password_code']
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
        data['message'] = list(Forgotpasswordform.errors.values())[0][0]
    return JsonResponse(data)
