#Login view and Logout view is taken care by importing views from django.contrib.auth
from django.contrib.auth import views as auth_views

from django.urls import path, include
from . import views

app_name = 'accounts' #needed for url templates..
#in order to make references that are app specific in templates

urlpatterns = [
    path('login/',
         auth_views.LoginView.as_view(template_name = 'accounts/login.html'),
         name = 'login'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name = 'logout'),
    path('signup/',
         views.SignUp.as_view(),
         name = 'signup'),
    path('settings/',
         views.UserSettings.as_view(),
         name = 'userSettings'),
    path('settings/bookmarks/',
         views.BookmarkSettings.as_view(),
         name = 'bookmarkSettings'),
]
