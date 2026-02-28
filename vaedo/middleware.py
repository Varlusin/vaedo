from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import activate, get_language
from django.conf import settings

class LocaleMiddlewareCostum(MiddlewareMixin):
    def process_request(self, request):
        language=(
            request.COOKIES.get('language') or
            request.headers.get('Content-Language') or
            getattr(request, 'session', {}).get('Language') or
            settings.LANGUAGE_CODE
        )
        if get_language() != language:
            activate(language)
        request.LANGUAGE_CODE=language
    def process_response(self, request, response):
        language = get_language()
        if request.COOKIES.get('language')!=language:
            response.set_cookie("language", language, max_age=31536000)
        response.headers.setdefault("Content-Language", language)
        return response