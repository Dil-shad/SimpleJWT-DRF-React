from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
import jwt
from datetime import datetime, timedelta
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# Custom TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

# Custom TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = self.context['request'].data.get(
            'refresh')  # Get the refresh token value

        try:
            refresh_token = RefreshToken(refresh)
            user_id = refresh_token.payload.get('user_id')
            user = User.objects.get(id=user_id)  # Retrieve the user object
        except:
            raise ValidationError('Invalid refresh token')

        access_token = refresh_token.access_token

        # Create custom claims for the access token
        access_token.payload['username'] = user.username

        # ...

        # Generate refreshed access token and return both tokens
        new_access_token = AccessToken.for_user(user)
        new_access_token['username'] = user.username
        new_refresh_token = RefreshToken.for_user(user)

        return {'access': str(new_access_token), 'refresh': str(new_refresh_token)}

# No changes needed in CustomTokenRefreshView class


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
