import re

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import resolve

PUBLIC_PATHS = [r'^/signin/$', r'^/signup/$', r'^/logout/$']





class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if any(re.match(path, request.path_info) for path in PUBLIC_PATHS):
            return
        access_token_cookie = request.COOKIES.get('access_token')
        if access_token_cookie:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token_cookie}'

    def process_response(self, request, response):
        if response.status_code == 401:
            refresh_token_cookie = request.COOKIES.get('refresh_token')

            if refresh_token_cookie:
                try:
                    refresh = RefreshToken(refresh_token_cookie)
                    new_access_token = str(refresh.access_token)
                    new_refresh_token = str(refresh)

                    new_response = HttpResponseRedirect(request.get_full_path())

                    new_response.set_cookie(
                        'access_token', new_access_token,
                        httponly=True, samesite='Lax', secure=False  # secure=True в проде
                    )

                    new_response.set_cookie(
                        'refresh_token', new_refresh_token,
                        httponly=True, samesite='Lax', secure=False  # secure=True в проде
                    )

                    return new_response

                except TokenError:
                    response.delete_cookie('access_token')
                    response.delete_cookie('refresh_token')
                    return response

        return response