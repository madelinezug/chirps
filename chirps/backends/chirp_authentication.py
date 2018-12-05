from django.contrib.auth.models import User
from announcements.models import Individual
from django.core.exceptions import ObjectDoesNotExist

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey


class ChirpAuthBackend:
    
    def authenticate(self, request, username=None, password=None):
        try:
            print("CHIRP AUTH")
            user = Individual.objects.get(pk=username)
            actual = user.chirp_pass
            input_pass = bytes(password, encoding='utf-8')
            backend = default_backend()
            salt = user.chirp_salt
            key_gen = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=backend
            )
            key_gen.verify(input_pass, actual)
            return User.objects.get(username=username)
        except (ObjectDoesNotExist, InvalidKey):
            return None

    def get_user(self, user_id):
        try:
            print("CHIRP GET USER")
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
