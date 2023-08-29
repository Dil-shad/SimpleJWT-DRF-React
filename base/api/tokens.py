import jwt
from rest_framework_simplejwt.tokens import RefreshToken


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
