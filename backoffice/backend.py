from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import check_password
from django.contrib.auth.hashers import check_password

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        user_model = get_user_model()
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = user_model.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                return None
        except user_model.DoesNotExist:
            return None

    def get_user(self, id=None):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=id)
        except user_model.DoesNotExist:
            return None