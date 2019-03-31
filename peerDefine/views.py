from django.views.generic import TemplateView
from django.shortcuts import render
from dal import autocomplete
from terms.models import Term
import json
from definitions.models import Definition
from django.core.serializers.json import DjangoJSONEncoder
import tagulous
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from definitions.models import Definition
from definitions.models import Authors
from django.http import HttpResponse
from django.db.models import Count

# Login Success (Update... very basic at the moment)
class TestPage(TemplateView):
    template_name = 'test.html'

# Logout page (Update... very basic at the moment)
class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class AboutUs(TemplateView):
    template_name = 'about_us.html'

class Privacy_Page(TemplateView):
    template_name = 'privacy_page.html'
class HomePage(TemplateView):
    template_name = 'index.html'
# Code adapted from irene, answered on Feb 9 '17 at 6:10
# https://stackoverflow.com/questions/42129331/how-to-pass-objects-to-a-templateview
    def get_context_data(self, **kwargs):
         #Gathering definitions
         definitions = Definition.objects.all().prefetch_related('author').order_by('citeNumber')

         # top cited, most followed, and most recent definition (for panels under search bar in index)
         definitionsTopCit = definitions.order_by('-citeNumber')[:3]
         defsMostFollowed = definitions.annotate(num_Follwing=Count('usersFollowing')).order_by("-num_Follwing")[:3]
         defsMostRecent = definitions.order_by('-created_at')[:3]

         #Gathering terms
         terms = Term.objects.all().prefetch_related('definitions')

         # top cited, most followed, and most recent terms (for panels under index search bar)
         termsMostDefs = terms.annotate(num_Defs=Count('definitions')).order_by("-num_Defs")[:3]
         termsMostFollowed = terms.annotate(num_Follwing=Count('usersFollowing')).order_by("-num_Follwing")[:3]
         termsMostRecent = terms.order_by('-id')[:3]

         context = super(HomePage,self).get_context_data(**kwargs)
         context['defTopCit'] = definitionsTopCit
         context['defMostFollowed'] = defsMostFollowed
         context['defMostRecent'] = defsMostRecent
         context['termMostDefs'] = termsMostDefs
         context['termMostFollowed'] = termsMostFollowed
         context['termMostRecent'] = termsMostRecent
         return context


# Used for autocomplete in search bars
def get_terms(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    terms = Term.objects.filter(name__icontains=q)
    results = []
    for pl in terms:
      term_json = pl.name
      results.append(term_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)


# Used to update user notifications in navbar
@login_required
def get_notifications_ajax(request):
	if request.is_ajax() and request.method == "POST":
		notifications = Notification.objects.filter(unread=1, recipient=request.user)
		count = notifications.count()
		notes = []
		for note in notifications:
			notes.append(str(note.verb))
		data = {
			"notifications": notes,
			"count": count,
		}
		print(data)
		json_data = json.dumps(data)
		print(json_data)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404


# Marks all notifications as read
@login_required
def all_Read(request):
    notifications = Notification.objects.filter(recipient=request.user)
    context={"notifications":notifications,}
    notifications.mark_all_as_read()
    return render(request, "notifications/all.html", context)

@login_required
def delete_all_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    context={"notifications":notifications,}
    notifications.delete()
    return render(request, "notifications/all.html", context)
