from rest_framework_simplejwt.views import TokenRefreshView
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response


def create_jwt_pair_for_user(user):
    refresh = RefreshToken.for_user(user)

    # Create custom payload with username
    payload = {
        "user_id": user.id,
        "username": user.username,
        "access_exp": refresh.access_token.payload["exp"],
        "refresh_exp": refresh.payload["exp"],
    }

    # Create access token with custom payload
    access_token = jwt.encode(payload, 'secret', algorithm="HS256")

    tokens = {"access": access_token, "refresh": str(refresh)}

    return tokens


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Invalid refresh token"}, status=400)

        old_refresh_token = RefreshToken(refresh_token)
        user_id = old_refresh_token.payload.get('user_id')
        if user_id is None:
            return Response({"error": "Invalid refresh token"}, status=400)

        user = User.objects.get(id=user_id)
        refresh = RefreshToken.for_user(user)
        payload = {
            "user_id": user.id,
            "username": user.username,
            "access_exp": refresh.access_token.payload["exp"],
            "refresh_exp": refresh.payload["exp"],
        }
        new_access_token = jwt.encode(payload, 'secret', algorithm="HS256")
        new_refresh_token = RefreshToken.for_user(user)

        return Response({
            "access": str(new_access_token),
            "refresh": str(new_refresh_token)
        })
