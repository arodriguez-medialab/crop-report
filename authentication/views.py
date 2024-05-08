from django.shortcuts import render
from authentication.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
from authentication.graph_helper import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import os

def login_view(request):
    return render(request, 'authentication/login.html')

@login_required(login_url="/login/")
def home(request):
    context = initialize_context(request)
    return render(request, 'report/welcome.html', context)

def initialize_context(request):
    context = {}
    error = request.session.pop('flash_error', None)
    if error != None:
        context['errors'] = []
        context['errors'].append(error)
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context

def sign_in(request):
    authenticate(request, mode="user")
    return HttpResponseRedirect(request.session['auth_flow']['auth_uri'])

def admin_sign_in(request):
    authenticate(request, mode="admin")
    return HttpResponseRedirect(request.session['auth_flow']['auth_uri'])

def graph_sign_in(request, mode):
    flow = get_sign_in_flow()
    try:
        request.session['auth_flow'] = flow
        request.session['mode'] = mode
    except Exception as e:
        print(e)

def callback(request):
    result = get_token_from_code(request)
    user = get_user(result['access_token'])
    if "error" in user:
      return HttpResponseRedirect(reverse('signout'))
    store_user(request, user)
    user = authenticate(request, username = user["userPrincipalName"], code = request.session['code_verifier'])
    mode = request.session.pop('mode', {})
    code_verifier = request.session.pop('code_verifier', {})
    if user:
      login(request, user)
      if mode == "admin":
          return HttpResponseRedirect("/admin")
      else:
          return HttpResponseRedirect(reverse('home'))
    else:
      return HttpResponseRedirect(reverse('signout'))

def sign_out(request):
    logout(request)
    remove_user_and_token(request)
    return HttpResponseRedirect(os.getenv('LOGOUT_REDIRECT_URL', "https://login.microsoftonline.com/common/oauth2/v2.0/logout?post_logout_redirect_uri=https://crop-report.agritop.net/login/"))
