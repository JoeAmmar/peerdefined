"""peerDefine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#Package related
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
import tagulous.views
import notifications.urls

# Model-related
from peerDefine import views
from terms import views as viewz
import definitions.models as definitionModel


urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')), #alt admin. Used for lookups autocompletes
    path('nested_admin/', include('nested_admin.urls')), # nested admin
    path('', views.HomePage.as_view(), name='home'),
    path('about_us/', views.AboutUs.as_view(), name = 'aboutus'), # Login Success: need to update later (very basic)
    path('privacy/', views.Privacy_Page.as_view(), name = 'privacy_page'),
    path('accounts/', include('accounts.urls', namespace = 'accounts')), #Removed for django-allauth version below
    path('accounts/', include('allauth.urls')),
    path('terms/', include('terms.urls', namespace = 'terms')),
    path('definitions/', include('definitions.urls', namespace='definitions')),
    path('accounts/', include('django.contrib.auth.urls')), #needed for additional built-in authentication stuff
    path('success/', views.TestPage.as_view(), name = 'test'), # Login Success: need to update later (very basic)
    path('thanks/', views.ThanksPage.as_view(), name='thanks'), # Logout Success:need to update later (very basic)
    path('api/get_terms/', views.get_terms, name='get_terms'), # Used for autocomplete in search bar
    re_path(r'^api/synonyms/$',tagulous.views.autocomplete, #Autocomplete for synonyms input for Definition form
            {'tag_model': definitionModel.Synonym},
            name='definition_synonym_autocomplete'),
    re_path(r'^api/discipline/$',tagulous.views.autocomplete, #Autocomplete for synonyms input for Definition form
            {'tag_model': definitionModel.Discipline},
            name='definition_discipline_autocomplete'),
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')), # inbox for all notifications
    re_path(r'^notifications/ajax/$',views.get_notifications_ajax, name='get_notifications_ajax'), #Get notifications for user (for navbar: updates automatically)
    re_path('^inbox/notifications_all/', views.all_Read, name='all_Read'), # Marks all notifications as read
    re_path('^inbox/delete_all_notifications/', views.delete_all_notifications, name='delete_all_notifications'),
]


# DEBUG TOOLBAR
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
