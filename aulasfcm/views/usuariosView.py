from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    extra_context = {'done': 'done'}

