from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
User = get_user_model()
from authentication.views import graph_sign_in

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, mode=None, code=None):
        if mode == "user" or mode == "admin":
            graph_sign_in(request, mode)
        elif username != None and code != None:
            if code != request.session['code_verifier']:
                return None
            try:
                user = User.objects.get(username=username.lower())
                return user
            except User.DoesNotExist:
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
