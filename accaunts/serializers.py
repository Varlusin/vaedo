from accaunts.models import UserModel
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField

from django.utils.translation import gettext_lazy as _

class UserModelSerializer(serializers.Serializer):
    username=serializers.CharField(help_text=_("Մուտքանուն"))
    password=serializers.CharField(write_only=True, help_text=_("Գաղտնաբառ"))

class LoginSerializer(UserModelSerializer):
    def validate(self, data):
        if not data.get('username'):
            raise serializers.ValidationError({'username': _("Մուտքագրեք անունը")})
        if not data.get('password'):
            raise serializers.ValidationError({'password': _("Մուտքագրեք գաղտնաբառը")})
        if not UserModel.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({'username': _("Այս անունը գոյություն չունի")})
        if not UserModel.objects.filter(password=data.get('password')).exists():
            raise serializers.ValidationError({'password': _("Գաղտնաբառը սխալ է")})
        return data





class RegisterSerializer(UserModelSerializer):
    first_name=serializers.CharField(help_text=_("Անուն"))
    last_name=serializers.CharField(help_text=_("Ազգանուն"))
    email=serializers.EmailField(help_text=_("Էլ. հասցե"))
    password_2=serializers.CharField(write_only=True, help_text=_("Գաղտնաբառ կրկին"))
    phone=PhoneNumberField(help_text=_("Հեռախոսահամար"))
    def validate(self, data):
        if data['password']!=data['password_2']:
            raise serializers.ValidationError({
                'password': _("Գաղտնաբառերը չեն համընկնում"),
                'password_2': _("Գաղտնաբառերը չեն համընկնում"),
                })
        if len(data['password'])<6:
            raise serializers.ValidationError({'password': _("Գաղտնաբառը պետք է լինի առնվազն 8 նիշ")})
        # if not any(char.isdigit() for char in data['password']):
        #     raise serializers.ValidationError({'password': _("Գաղտնաբառը պետք է պարունակի թվեր")})
        # if not any(char.isalpha() for char in data['password']):
        #     raise serializers.ValidationError({'password': _("Գաղտնաբառը պետք է պարունակի տառեր")})
        # if not any(char.isupper() for char in data['password']):
        #     raise serializers.ValidationError({'password': _("Գաղտնաբառը պետք է պարունակի մեծատառեր")})
        # if not any(char.islower() for char in data['password']):
        #     raise serializers.ValidationError({'password': _("Գաղտնաբառը պետք է պարունակի փոքրատառեր")})
        # if not any(char in ['!', '@', '#', '$', '%', '^', '&', '*'] for char in data['password']):
        #     raise serializers.ValidationError({'password': _("Գաղտնաբառը պետք է պարունակի հատուկ նիշեր")})
        if UserModel.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': _("Անունը արդեն գրանցված է")})
        
        if UserModel.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': _("Էլ. հասցեն արդեն գրանցված է")})
        data.pop('password_2')
        return data
    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
    
    def save(self, **kwargs):   
        user=self.create(self.validated_data)
        user.set_password(self.validated_data['password'])
        user.save()
        return user   


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token=super().get_token(user)
        token['Name']=user.first_name
        return token

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data=super().validate(attrs)
        # refresh = RefreshToken(attrs['refresh'])
        # data['Name']= refresh.payload.get('Name', '')
        return data

class GooglecodeSerializer(serializers.Serializer):
    code=serializers.CharField()



