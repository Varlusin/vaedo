# from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework.exceptions import AuthenticationFailed

from accaunts.models import UserModel
from accaunts.serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class GetprofileView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            menu = [
                {
                    "url": "/profile/edit/",
                    "Value": _("Փոփոխել"),
                    "imgUrl": "/static/main/img/change_profile.svg",
                },
                {
                    "url": "/logout/",
                    "Value": _("Դուրս գալ"),
                    "imgUrl": "/static/main/img/logout.svg",
                },
            ]
            return Response(
                {"authenticated": True, "name": user.first_name, "menu": menu},
                status=status.HTTP_200_OK,
            )
        menu = [
            {
                "url": "/login/",
                "Value": _("Մուտք"),
                "imgUrl": "/static/main/img/login.svg",
            },
            {
                "url": "/register/",
                "Value": _("Գրանցվել"),
                "imgUrl": "/static/main/img/registration.svg",
            },
        ]
        return Response(
                {"authenticated": False, "menu": menu},
                status=status.HTTP_200_OK,
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get the tokens
        tokens = serializer.validated_data
        # Set the cookies
        response = Response(tokens, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=tokens["access"],
            httponly=True,
            secure=True,
            samesite='None',
        )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer





class RegisterViewset(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ["post","get"]
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        fields = serializer.fields  # Ստանում ենք serializer-ի դաշտերը
        form_fields = {
            field_name: {
                "type": field.__class__.__name__,
                "required": field.required,
                "help_text": getattr(field, "help_text", ""),
            }
            for field_name, field in fields.items()
        }
        extra_data = {
            "form_title": _("Գրանցման ձև"),
            "submit_button_text": _("Գրանցվել"),
        }
        return Response({"fields": form_fields, **extra_data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token_data = {
                "username": request.data.get("username"),
                "password": request.data.get("password"),
            }
            token_serializer = CustomTokenObtainPairSerializer(data=token_data)
            if token_serializer.is_valid():

                responce =  Response(
                    {
                        "user": serializer.data,
                        "accessToken": token_serializer.validated_data['access'],
                    }
                )
                responce.set_cookie(
                    key="refresh_token",
                    value=token_serializer.validated_data['refresh'],
                    httponly=True,
                    secure=True,
                    samesite='None',
                )
                responce.set_cookie(
                    key="access_token",
                    value=token_serializer.validated_data['access'],
                    httponly=True,
                    secure=True,
                    samesite='None',
                )
                return responce
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            token = request.data["refresh"]
            token_obj = RefreshToken(token)
            token_obj.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
