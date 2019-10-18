#Login view and Logout view is taken care by importing views from django.contrib.auth
from django.contrib.auth import views as auth_views

from django.urls import path, include, re_path
from . import views

app_name = 'terms'


urlpatterns = [
    re_path(r"^$", views.ListTerms.as_view(), name="all"),
    re_path(r"^new/$", views.CreateTerm.as_view(), name="create"),
    path('search/', views.TermSearchListView.as_view(), name='term_search_list_view'),
    re_path(r'^(?P<term_id>\d+)/follow$', views.followTerm, name="follow_term"),
    re_path(r'^api$', views.TermAPI.as_view(), name="term_API"),
    re_path(r'^api/(?P<query>[-\w]+)$', views.TermSearchAPI.as_view(), name="term_search_API"),
]
