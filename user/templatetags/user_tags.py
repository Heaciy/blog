from urllib.parse import urlencode
from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag

def get_login_github_url():
    params = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'redirect_uri': settings.GITHUB_REDIRECT_URL,
        'state': settings.GITHUB_STATE,
    }
    return 'https://github.com/login/oauth/authorize?' + urlencode(params)