#importing from packages
import base64 #citation code
from braces.views import LoginRequiredMixin, UserFormKwargsMixin, SelectRelatedMixin
import django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.db.models import Q
from django.db.models import Case, IntegerField, Value, When
from django.http import Http404,HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from extra_views import InlineFormSet, CreateWithInlinesView, UpdateWithInlinesView, NamedFormsetsMixin#, InlineFormSetView
from habanero import cn, Crossref
import http.client # citationCode
import json
from notifications.signals import notify
import reversion
from reversion.models import Version
import tagulous
import urllib.request # citationCode
import urllib.parse # citationCode
import urllib.error # citationCode


# importing from models and forms
from definitions import models
from definitions import forms
from terms.models import Term


# Getting user model
User = get_user_model()


#Defitions List for Specific User
# NEEDS TEMPLATE UPDATE
class UserDefinitions(generic.ListView):
    model = models.Definition
    template_name = 'definitions/user_definition_list.html'

    def get_queryset(self):
        try: #get related definitions to a user
            self.definition_user = User.objects.prefetch_related('definitions').get(username__iexact = self.kwargs.get('username'))
            # we can add __ and commands like 'iexact' (isexactly)
            # prefetch_related is used instead of select_related when we have many-to-many relationship

        except User.DoesNotExist:
            raise Http404
        else:
            return self.definition_user.definitions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['definition_user'] = self.definition_user
        return context


# Form (Creation of New Definition)

# Creating inline form with Author Model
class AuthorsInline(InlineFormSet):
    model = models.Authors
    fields = ('doi','in_text', 'citation')
    form_class = forms.AuthorsForm
    factory_kwargs = {'max_num': 1, 'can_delete': False}

# Definition Creation Class-Based View
# With Authors inline
class DefinitionCreateView(CreateWithInlinesView, UserFormKwargsMixin, LoginRequiredMixin, SelectRelatedMixin, NamedFormsetsMixin):
    inlines = [AuthorsInline]
    inlines_names = ['authors']
    model = models.Definition
    form_class = forms.DefinitionForm
    formset_class = forms.AuthorsForm

    def get_context_data(self, **kwargs):
        context = super(DefinitionCreateView, self).get_context_data(**kwargs)
        term = Term.objects.get(id=self.kwargs["term_id"])
        context['term_name'] = term.name
        return context

    def forms_valid(self, form, inlines):
        # add the initial value here
        # but first get the id from the request GET data,
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.original_user = self.request.user
        self.object.term = Term.objects.get(id=self.kwargs["term_id"])
        self.object.save()

        # This section creates the description for notifications (for users following a definition or term)
        # It's used on the notifications screen to allow url to redirect to the
                # term (if user does not have access to def history)

        # Insert whitespace between termId and termslug in order to extract each properly
        blankTimes = 10-len(str(self.object.id))
        blanks = ""
        for d in range(0,blankTimes):
            blanks = blanks + " "

        termSlugId = str(self.object.id) + blanks + self.object.term.slug

        #Extract users following a term from which definition originates
        termFollow = self.object.term.usersFollowing.all().exclude(username=self.request.user)

        #Send notification to users following term associated with this definition.
        notify.send(sender = self.request.user,
                        recipient=termFollow,
                         verb=str(self.request.user) + ' created a new definition in ' + str(self.object.term.name) + ' (' + inlines[0][0]['in_text'][0].data['value'] + ')',
                         description=termSlugId)
        return super().forms_valid(form, inlines)


class DeleteDefinition(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Definition
    select_related = ('user', 'term', 'original_user')
    prefetch_related = ('author', "discipline", "synonym")

    # only shows definition deletion page if user is the original creator or a superuser
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(original_user_id=self.request.user.id)
        return queryset

    # if succesfully deleted, go back to associated term's definition list
    def get_success_url(self):
        term = self.object.term
        return reverse_lazy('definitions:term_single', kwargs ={'termSlug':term.slug})

    # deletion logic
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        # only allows deletion for original user or a superuser
        if self.object.original_user == self.request.user or self.request.user.is_superuser:
            messages.success(self.request, 'definition Deleted')
            return super().delete(*args, **kwargs)
        else:
            raise ArithmeticError("You are not the original user")


class UpdateDefinition(UpdateWithInlinesView, LoginRequiredMixin):
    inlines = [AuthorsInline]
    inlines_names = ['authors']
    model = models.Definition
    form_class = forms.DefinitionForm
    formset_class = forms.AuthorsForm

    def get_context_data(self, **kwargs):
        context = super(UpdateDefinition, self).get_context_data(**kwargs)
        term = Term.objects.get(id=self.kwargs["term_id"])
        context['term_name'] = term.name
        return context

    def get_queryset(self):
        queryset = super(UpdateDefinition, self).get_queryset()
        return queryset

    def forms_valid(self, form, inlines):
        #Originally only allowed original users and admins to edit
        #Now anyone can update a definition
        self.object = form.save(commit=False)
        self.object.lastModifiedUser = self.object.user
        self.object.user = self.request.user
        self.object.term = Term.objects.get(id=self.kwargs["term_id"])
        self.object.save()

        # This section creates the description for notifications (for users following a definition or term)
        # It's used on the notifications screen to allow url to redirect to the
                # term (if user does not have access to def history)

        # Insert whitespace between termId and termslug in order to extract each properly

        blankTimes = 10-len(str(self.object.id))
        blanks = ""
        for d in range(0,blankTimes):
            blanks = blanks + " "

        termSlugId = str(self.object.id) + blanks + self.object.term.slug

        # Extracts userlist of those who favorited this definition or the associated term
        # excludes the original creator and the last person who modified the definition
        defFollow = self.object.usersFollowing.all().exclude(username=self.request.user).exclude(username=self.object.original_user).exclude(username=self.object.lastModifiedUser)
        termFollow = self.object.term.usersFollowing.all().exclude(username=self.request.user).exclude(username=self.object.original_user).exclude(username=self.object.lastModifiedUser).exclude(username__in=list(defFollow))

        # combines both user lists
        termDefFollow = termFollow | defFollow

        # Notifies original creator that someone modified their definition (if someone else modified it)
        if self.object.original_user != self.request.user:
            notify.send(sender = self.request.user,
                        recipient=self.object.original_user,
                         verb=str(self.request.user) + ' modified your definition for ' + str(self.object),
                         description=self.object.id)

        # Notifies user who last modified this definition that it's been changed
        if self.object.lastModifiedUser != self.request.user and self.object.lastModifiedUser != self.object.original_user:
            notify.send(sender = self.request.user,
                        recipient=self.object.lastModifiedUser,
                         verb=str(self.request.user) + ' modified the definition for ' + str(self.object),
                         description=self.object.id)

        # Also notifies users who follow (favorited) this definition that it's been changed
        notify.send(sender = self.request.user,
                    recipient=termDefFollow,
                    verb=str(self.request.user) + ' modified the definition of ' + str(self.object),
                    description=termSlugId)
        return super().forms_valid(form, inlines)


#Class-based View for List of Definitions For A Term
class TermDefListView(SelectRelatedMixin, generic.ListView):
    model = models.Definition
    select_related = ('user', 'term', 'usersFollowing', 'original_user')
    prefetch_related = ('author', "discipline", "synonym")
    template_name = 'definitions/definition_term_list.html'
    def get_queryset(self):
        return models.Definition.objects.select_related('user', 'term', 'original_user').prefetch_related('author', "discipline", "synonym").filter(term__slug=self.kwargs['termSlug']).distinct().order_by('term', '-citeNumber')

    def get_context_data(self, **kwargs):
        context = super(TermDefListView, self).get_context_data(**kwargs)
        # Getting Term instance from Model to gain info about the users following this term
        termFull = models.Term.objects.filter(slug=self.kwargs['termSlug']).distinct().first()

        termId = termFull.id

        # Setting term slug, term_id, and whether term is favorited by user into context
        context['termSlug'] = self.kwargs.get('termSlug')
        context['term_Id'] = termId
        context['favoritedterm'] = self.request.user in termFull.usersFollowing.all()
        return context

# Class-based view for Definitions based on Synonyms
class SynSearchListView(SelectRelatedMixin, generic.ListView):
    model = models.Definition
    select_related = ('user', 'term', 'original_user')
    prefetch_related = ('author', "discipline", "synonym")
    template_name = 'definitions/definition_syn_list.html'

    def get_queryset(self):
        result = super(SynSearchListView, self).get_queryset()
        synonymSynonyms = result.filter(term__slug=self.kwargs['synSlug']).distinct()
        #Error if no definitions exist for synonym
        if not synonymSynonyms:
            raise exceptions.FieldDoesNotExist("The synonym you clicked (" + self.kwargs['synSlug'] + ") does not have any definitions yet.")
        synList = []

        #List of terms that contain a definition that lists the synonym term as a synonym
        for syns in synonymSynonyms:
            if tagulous.utils.parse_tags(syns.synonym):
                parsedTag = tagulous.utils.parse_tags(syns.synonym)[0]
                synList.append(parsedTag)

        # Create list of defs for synonym term and related terms
        result = models.Definition.objects.select_related('user', 'term', 'original_user').prefetch_related('author', "discipline", "synonym").filter(Q(term__slug__iexact=self.kwargs['synSlug']) | Q(synonym__slug__icontains=self.kwargs['synSlug']) | Q(term__name__in=synList)).annotate(synvar=Case(
        When(Q(term__slug=self.kwargs['synSlug']) | Q(term__slug=self.kwargs['synSlug'].lower()) | Q(term__slug=self.kwargs['synSlug'].title()), then=Value(0)),
        default=Value(1),
        output_field=IntegerField()
        )).order_by('synvar', 'term', '-citeNumber').distinct()
        return result

    def get_context_data(self, **kwargs):
        context = super(SynSearchListView, self).get_context_data(**kwargs)
        context['synSlug'] = self.kwargs.get('synSlug')
        return context


# Class-based view for Definitions based on Disciplines
class DiscSearchListView(SelectRelatedMixin, generic.ListView):
    model = models.Definition
    select_related = ('user', 'term', 'original_user')
    prefetch_related = ('author', "discipline", "synonym")
    template_name = 'definitions/definition_disc_list.html'

    #Get definitions that fall under a specified discipline
    def get_queryset(self):
        result = super(DiscSearchListView, self).get_queryset()
        return result.filter(discipline__slug=self.kwargs['discSlug']).distinct().order_by('term', '-citeNumber')

    #Adding DiscSlug context variable for template
    def get_context_data(self, **kwargs):
        context = super(DiscSearchListView, self).get_context_data(**kwargs)
        context['discSlug'] = self.kwargs.get('discSlug')
        return context



# Gets history of a definition

@login_required
def get_history_Definition(request, pk):
    #The following commented code might be required by django reversion
        #   django.contrib.admin.autodiscover()

    template = 'definitions/definition_history.html'

    # ma refers to definition model objects
    # auth is used for authors model (to edit it along with definition model)
    ma = get_object_or_404(models.Definition.objects, pk=pk)
    auth = get_object_or_404(models.Authors.objects.filter(definitions__pk=pk))

    #only allows original users or admins to review history
    if not (ma.original_user == request.user or request.user.is_superuser):
        raise ArithmeticError("You are not the original user") #change the error type later
    else:
        version_authors = Version.objects.get_for_object(auth)
        version_list = Version.objects.get_for_object(ma)
        for ver in version_list:
            #Adding fields so history page shows more information about each definition (authors[actually article meta-data], synonyms, and disciplines)
            rev_id = ver.revision_id
            qsyn = json.loads(ver.serialized_data)[0]['fields']['synonym']
            qdisc = json.loads(ver.serialized_data)[0]['fields']['discipline']
            ver.synonym = ", ".join(qsyn)
            ver.discipline = ", ".join(qdisc)
            for ver_auth in version_authors:
                if ver_auth.revision_id == rev_id:
                    qs = json.loads(ver_auth.serialized_data)[0]
                    ver.in_text = qs['fields']['in_text']
                    ver.citation = qs['fields']['citation']

        # code below paginates list of modifications on history page
        # adapted heavily from https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
        # author: Vitor Freitas (Aug 3, 2016)

        paginator = Paginator(version_list, 10)
        page = request.GET.get('page', 1)
        try:
            version_list = paginator.page(page)
        except PageNotAnInteger:
            version_list = paginator.page(1)
        except EmptyPage:
            version_list = paginator.page(paginator.num_pages)
        context = { 'obj_pk': pk, 'version_list': version_list}
        return render(request, template, context)

@login_required
def revert_definitions_to_revision(request, pk, rev_pk):
    ma = get_object_or_404(models.Definition.objects.prefetch_related("author", "synonym", "discipline"), pk=pk)
    version_check = Version.objects.get_for_object(ma)
    version = Version.objects.get_for_model(ma).get(id=rev_pk)

    #Only allow original users and superuser to make revisions
    if not (ma.original_user == request.user or request.user.is_superuser):
        raise ArithmeticError("You are not the original user") #change the error type later
    else:


        # This section creates the description for notifications (for users following a definition or term)
        # It's used on the notifications screen to allow url to redirect to the
                # term (if user does not have access to def history)

        # Insert whitespace between termId and termslug in order to extract each properly

        blankTimes = 10-len(str(ma.id))
        blanks = ""
        for d in range(0,blankTimes):
            blanks = blanks + " "

        termSlugId = str(ma.id) + blanks + ma.term.slug

        # Extracts userlist of those who favorited this definition or the associated term
        # excludes the original creator and the last person who modified the definition
        defFollow = ma.usersFollowing.all().exclude(username=request.user).exclude(username=ma.original_user).exclude(username=ma.user)
        termFollow = ma.term.usersFollowing.all().exclude(username=request.user).exclude(username=ma.original_user).exclude(username=ma.user).exclude(username__in=list(defFollow))

        # combines both user lists
        termDefFollow = termFollow | defFollow

        # Notifies original creator that someone modified their definition (if someone else modified it)
        if ma.original_user != request.user:
            notify.send(sender = request.user,
                        recipient=ma.original_user,
                         verb=str(request.user) + ' modified your definition for ' + str(ma),
                         description=ma.id)

        # Notifies user who last modified this definition that it's been changed
        if ma.user != request.user and ma.user != ma.original_user:
            notify.send(sender = request.user,
                        recipient=ma.user,
                         verb=str(request.user) + ' modified the definition for ' + str(ma),
                         description=ma.id)

        # Also notifies users who follow (favorited) this definition that it's been changed
        notify.send(sender = request.user,
                    recipient=termDefFollow,
                    verb=str(request.user) + ' modified the definition of ' + str(ma),
                    description=termSlugId)

        # Blocks attempts to revert model from current version to current version
        if str(version_check[0].id) != str(rev_pk):
            with transaction.atomic(), reversion.create_revision():
                reversion.set_comment("reverted Definition")
                reversion.set_user(request.user)
                version.revision.revert()

        else:
            raise ArithmeticError(rev_pk)
            #returns list of definitions for relevant term
    return HttpResponseRedirect(reverse_lazy('definitions:term_single', args=(ma.term.slug,)))

# Get definitions objects for Timeline
def get_all_definitions(request, termSlug):
    if request.is_ajax() and request.method == "POST":
        definitions = models.Definition.objects.all().select_related('user', 'term', 'original_user').prefetch_related('author', "discipline", "synonym").filter(term__slug = termSlug).order_by('year')
        results = []
        #getting Definition objects ready to format into JSON
        for defs in definitions:
            d = [defs.term.name,
                 str(defs.author.all()[0]),
                 defs.defs,
                 defs.year, defs.citeNumber]
            results.append(d)
        response = {
            'results':  results,
        }
        json_data = json.dumps(response)
        return HttpResponse(json_data, content_type='application/json')


# Get synonym objects for Timeline (for synonym-specific definitions pages)
def get_all_definitions_syn(request, synSlug):
    if request.is_ajax() and request.method == "POST":
        synonymSynonyms = models.Definition.objects.select_related('user', 'term', 'original_user').prefetch_related('author', "discipline", "synonym").filter(term__slug=synSlug).distinct()
        synList = []

        #List of terms that contain a definition that lists the synonym term as a synonym
        for syns in synonymSynonyms:
            if tagulous.utils.parse_tags(syns.synonym):
                parsedTag = tagulous.utils.parse_tags(syns.synonym)[0]
                synList.append(parsedTag)

        # getting a list of defs for synonym term and related term
        definitions = models.Definition.objects.select_related('user', 'term', 'original_user').prefetch_related('author', "discipline", "synonym").filter(Q(term__slug__iexact=self.kwargs['synSlug']) | Q(synonym__slug__icontains=self.kwargs['synSlug']) | Q(term__name__in=synList)).annotate(synvar=Case(
            When(Q(term__slug=self.kwargs['synSlug']) | Q(term__slug=self.kwargs['synSlug'].lower()) | Q(term__slug=self.kwargs['synSlug'].title()), then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
            )).order_by('year').distinct()
        results = []

        #getting Definition objects ready to format into JSON
        for defs in definitions:
            d = [defs.term.name,
                 str(defs.author.all()[0]),
                 defs.defs,
                 defs.year, defs.citeNumber]
            results.append(d)
        response = {
            'results':  results,
        }
        json_data = json.dumps(response)
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404

def get_all_definitions_disc(request, discSlug):
    if request.is_ajax() and request.method == "POST":
        #Getting definitions within a discipline
        definitions = models.Definition.objects.all().select_related('user', 'term', 'original_user').prefetch_related('author', "discipline", "synonym").filter(discipline__slug=discSlug).distinct().order_by('year')

        #getting Definition objects ready to format into JSON

        results = []
        for defs in definitions:
            d = [defs.term.name,
                 str(defs.author.all()[0]),
                 defs.defs,
                 defs.year, defs.citeNumber]
            results.append(d)
        response = {
            'results':  results,
        }
        json_data = json.dumps(response)
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


#### Following a definition (Favorites/Bookmarks Feature)
# The following code was adapted from erajuan
# answered Mar 17 '16 at 15:09
# edited Mar 17 '16 at 15:49
# https://stackoverflow.com/questions/36063984/django-how-to-follow-some-object-not-user

@login_required
def follow_definition(request,definition_id):
    user = request.user
    currentDefinition = models.Definition.objects.get(id=definition_id)

    # Conditional to see if user is the original creator
    # We don't want original users to be included in this list
    # Original users already get notified when anything happens to their definition

    if user != currentDefinition.original_user:
        # if user is currently following a definition, remove user from 'follow list'
        if user in currentDefinition.usersFollowing.all():
              currentDefinition.usersFollowing.remove(user)
        # adds user to follow list if they're not already in it
        else:
            currentDefinition.usersFollowing.add(user)
        currentDefinition.save()

        # shows user all the individuals who like a definition
        # used for JSON to update favorites list immediately (not just when page refreshes)
        # May want to edit in the future to keep user favorite list private
        userList = []
        for likes in currentDefinition.usersFollowing.all().values():
            userList.append(likes['username'])
        return HttpResponse(
                json.dumps({
                    "usersLike": userList,
                }),
                content_type="application/json"
            )
    else:
        return HttpResponse("You are the Original User", content_type='application/json')


## Citation Search (Microsoft Academic API) AJAX

@login_required
def citation_request(request):
    if request.is_ajax() and request.method == "POST":
        headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': settings.MICROSOFT_KEY,
        }
        qry = str(request.POST.get('qry')) #Get qry from ajax request
        params = urllib.parse.urlencode({
            # Request parameters
            'query': qry,
            'complete': '0',
            'count': '10',
            'model': 'latest',
        })
        try:
            # Request related to interpreting search entry
            conn = http.client.HTTPSConnection('api.labs.cognitive.microsoft.com')
            conn.request("GET", "/academic/v1.0/interpret?%s" %
                         params, "{body}", headers)
            response = conn.getresponse()
            encoding = response.info().get_content_charset('utf8')
            data = response.read().decode(encoding)
            jsons = json.loads(data)
            #print(jsons)
            conn.close()
            print("Microsoft API Request Sent!")
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        if(jsons['interpretations'] == []):
            # If Microsoft can't interpret search entry, then return flag == True (logic used in Ajax to switch to crossRef search)
          return HttpResponse(
                  json.dumps({'responseText': jsons,
                  'flag': 'True'
                  }),
                  content_type="application/json"
              )

        else:
            # var eval is what's used to search for the article
            eval = jsons['interpretations'][0]['rules'][0]['output']['value']
            #####################################
            # EVALUATE
            #####################################
            headers = {
                # Request headers
                'Ocp-Apim-Subscription-Key': settings.MICROSOFT_KEY,
            }
            params = urllib.parse.urlencode({
                # Request parameters
                'expr': eval,
                'model': 'latest',
                'count': '10',
                'offset': '0',
                'attributes': 'Ti,Y,CC,AA.AuN,AA.DAuN,AA.AuId,E.VFN,E.DN,J.JId,E.DOI,E.V,E.I,E.FP,E.LP,AA.S,E'
            })
            try:
                # request related to retrieving article
                conn = http.client.HTTPSConnection('api.labs.cognitive.microsoft.com')
                conn.request("GET", "/academic/v1.0/evaluate?%s" %
                             params, "{body}", headers)
                response = conn.getresponse()
                encoding = response.info().get_content_charset('utf8')
                data = response.read().decode(encoding)
                jsonsArt = json.loads(data)
                conn.close()
                return HttpResponse(
                        json.dumps({'responseText': jsonsArt,
                                    'flag': 'False' # logic telling ajax whether microsoft search failed (False == did not fail)
                        }),
                        content_type="application/json"
                    )
            except:
                raise ArithmeticError("Something Went Wrong") # error raised if something goes wrong with retrieving article meta-data
    else:
        raise Http404
