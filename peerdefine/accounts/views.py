from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms

# Create your views here.

class SignUp(CreateView):
    #UserCreateForm was made in forms.py prior to the creation of this class.
    form_class = forms.UserCreateForm

    #Reverse_lazy is used here so that the redirection is only executed...
    # after signup occurs. Otherwise it'll redirect without signing the user up.

    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class UserSettings(TemplateView):
    template_name = 'accounts/userSettings.html'


class BookmarkSettings(TemplateView,LoginRequiredMixin):
    template_name = 'accounts/bookmarkSettings.html'
