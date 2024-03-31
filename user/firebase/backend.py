from rest_framework import authentication
from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError, EmailVerification, EmailExists
from firebase_admin import auth, credentials
import firebase_admin
from user.models import User, Provider
import os
import json
from dokan.settings import DEBUG, BASE_DIR


try:
    # Firebase Admin SDK credentials
    if DEBUG:
        cred = credentials.Certificate(os.path.join(BASE_DIR, 'service-account.json'))
    else:
        cred = credentials.Certificate(json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT')))
    app = firebase_admin.initialize_app(cred)

except Exception:
    raise FirebaseError("Firebase Admin SDK credentials not found. Please add the path to the credentials file to the FIREBASE_ADMIN_SDK_CREDENTIALS_PATH environment variable.")



class FirebaseAuthenticationBackend(authentication.BaseAuthentication):
    keyword = 'Bearer'
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise NoAuthToken("No authentication token provided.")
        id_token = auth_header.split(' ').pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid authentication token provided.")
        if not id_token or not decoded_token:
            return None
        # email_verified = decoded_token.get('email_verified')
        # if not email_verified:
        #     raise EmailVerification("Email not verified. please verify your email address.")
        try:
            uid = decoded_token.get('uid')
        except Exception:
            raise FirebaseError("The user provided with auth token is not a firebase user. it has no firebase uid.")
        try:
            user = User.objects.get(email=decoded_token.get('email'))
            user.picture = decoded_token.get('picture')
            name = decoded_token.get('name').split(' ')
            user.first_name = " ".join(name[:-1])
            user.last_name = name[-1]
            if user.uid is None:
                user.uid = uid
                user.save()
            
            if user.provider != decoded_token.get('firebase').get('sign_in_provider'):
                try:
                    provider = user.providers.filter(name=decoded_token.get('firebase').get('sign_in_provider')).first()
                    if not provider:
                        Provider.objects.create(name=decoded_token.get('firebase').get('sign_in_provider'), user=user)
                except Exception as e:
                    raise e
        except User.DoesNotExist:
            user = User.objects.create_user(uid=uid, email=decoded_token.get('email'), provider=decoded_token.get('firebase').get('sign_in_provider'))
        except Exception as e:
            print("Error:", e)
        print(user)
        return (user, self)