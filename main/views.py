from django.shortcuts import render
from django.utils.translation import gettext as _
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils.translation import activate

# for social autg google
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client



def index(request):
    context = {"title" : _("Home")}
    return render(request, "main/index.html", context)

def registration(request):
    context = {"title" : _("Registration")}
    return render(request, "main/register.html", context)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/"  
    client_class = OAuth2Client


def set_language(request):
    language=request.GET.get('lang','en')
    activate(language)
    response= JsonResponse({'message': f"Language set to {language}"})
    response.set_cookie("language", language, max_age=31536000)
    return response