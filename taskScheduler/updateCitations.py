from apscheduler.schedulers.blocking import BlockingScheduler
import base64 #citation code
import django
from django.conf import settings
from django.contrib import messages
from django.http import Http404,HttpResponseRedirect, HttpResponse
import http.client # citationCode
import json
import os
import sys
import urllib.request # citationCode
import urllib.error # citationCode


# following block of code taken from:
# https://stackoverflow.com/questions/32590241/standalone-django-orm-default-settings-not-recognized
# author BigZ
# edited Apr 21 '16 at 17:54
sys.path.append('/path/to/django_project')
#from django_project import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peerDefine.settings')
django.setup()


# importing from models and forms
from definitions import models
from definitions import forms
from terms.models import Term



sched = BlockingScheduler()

@sched.scheduled_job('interval',days=7)
def citationCountUpdate():
    auths = models.Authors.objects.select_related('definitions').all()
    defs = models.Definition.objects.all()
    for auth in auths:
        if auth.doi is not None:
            doi = auth.doi
            crossSite = 'https://api.crossref.org/works/' + doi
            with urllib.request.urlopen(crossSite) as url:
                data = json.loads(url.read().decode())
                if data['message']['is-referenced-by-count'] is not None:
                    citCount = data['message']['is-referenced-by-count']
                    auth.definitions.citeNumber = citCount
                    defInstance = defs.get(pk=auth.definitions.pk)
                    defInstance.citeNumber = citCount
                    defInstance.save()


sched.start()
