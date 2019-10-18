from django.urls import path, re_path
from . import views
import tagulous.views
from . import models
from rest_framework import routers

app_name = 'definitions'

urlpatterns = [
    re_path(r"new/(?P<term_id>\d+)/$", views.DefinitionCreateView.as_view(), name="create"),
    re_path(r"by/(?P<username>[-\w]+)/$",views.UserDefinitions.as_view(),name="for_user"),
    re_path(r"delete/(?P<pk>\d+)/$",views.DeleteDefinition.as_view(),name="delete"),
    path("update/<int:pk>/<int:term_id>/", views.UpdateDefinition.as_view(), name="update"),
    re_path(r"^definitions/synonyms/(?P<synSlug>[-\w]+)/$", views.SynSearchListView.as_view(), name='synonym_search_list_view'),
    re_path(r"^in/(?P<termSlug>[-\w]+)/$",views.TermDefListView.as_view(),name="term_single"),
    re_path(r"^synonyms/(?P<synSlug>[-\w]+)/$", views.SynSearchListView.as_view(), name='synonym_search_list_view'),
    re_path(r"^discipline/(?P<discSlug>[-\w]+)/$", views.DiscSearchListView.as_view(), name='discipline_search_list_view'),
    re_path(r'^(?P<pk>\d+)/history/$', views.get_history_Definition, name='definition_history'),
    re_path(r'^(?P<pk>\d+)/revert/(?P<rev_pk>\d+)/$', views.revert_definitions_to_revision,
        name='definition_revert'),
    re_path(r'^all/ajax/(?P<termSlug>[-\w]+)/$',views.get_all_definitions, name='get_all_definitions'),
    re_path(r'^syn/ajax/(?P<synSlug>[-\w]+)/$',views.get_all_definitions_syn, name='get_all_definitions_syn'),
    re_path(r'^disc/ajax/(?P<discSlug>[-\w]+)/$',views.get_all_definitions_disc, name='get_all_definitions_disc'),
    re_path(r'^(?P<definition_id>\d+)/follow$', views.follow_definition, name="follow_definition"),

]
