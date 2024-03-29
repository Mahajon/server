from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from firebase_admin import auth  # Import firebase_admin library

class FirebaseAuthenticationBackend(BaseBackend):
    """
    Custom Django authentication backend for Firebase Authentication.
    """

    def authenticate(self, request, token=None):
        if not token:
            # No Firebase ID token provided
            return None

        try:
            # Verify the Firebase ID token
            decoded_token = auth.verify_id_token(token.split(' ')[1])
            uid = decoded_token['uid']
        except (ValueError, auth.InvalidIdTokenError) as e:
            print(f"Invalid Firebase ID token: {e}")
            return None

        # Try to find a Django user associated with the Firebase UID
        try:
            user = User.objects.get(firebase_uid=uid)
        except User.DoesNotExist:
            # Create a new Django user if one doesn't exist
            user = User.objects.create_user(
                username=f"firebase_user_{uid}",
                email=decoded_token.get('email', None),  # Use email if available
            )
            user.firebase_uid = uid
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# Add this to your settings.py (AUTHENTICATION_BACKENDS)
AUTHENTICATION_BACKENDS = [
    'yourproject.apps.auth.FirebaseAuthenticationBackend',
    # Include any other authentication backends you might have
]
