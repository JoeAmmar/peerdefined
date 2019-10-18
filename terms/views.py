# Package Related
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from functools import reduce
import json
import operator
from rest_framework import generics


# Model related
from terms.models import Term
from terms.serializers import TermSerializer
from definitions.models import Definition, Authors, Synonym, Discipline

# Views

class CreateTerm(LoginRequiredMixin, generic.CreateView):
    fields = ('name',) #what can a user edit?
    model = Term

class ListTerms(generic.ListView):
    model = Term
    paginate_by = 10

# Returns results of search from index or navbar
class TermSearchListView(ListTerms):
    """
    Display a List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(TermSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )

        return result


#### Following a Term
# The following code was adapted from erajuan
# answered Mar 17 '16 at 15:09
# edited Mar 17 '16 at 15:49
# https://stackoverflow.com/questions/36063984/django-how-to-follow-some-object-not-user

@login_required
def followTerm(request,term_id):
    user = request.user
    currentTerm = Term.objects.get(id=term_id)
    if user in currentTerm.usersFollowing.all():
          currentTerm.usersFollowing.remove(user)
    else:
        currentTerm.usersFollowing.add(user)
    currentTerm.save()
    userList = []
    for likes in currentTerm.usersFollowing.all().values():
        userList.append(likes['username'])
    return HttpResponse(
            json.dumps({
                "usersLike": userList,
            }),
            content_type="application/json"
        )


class TermAPI(generics.ListAPIView):
    """
    Retrieve all Terms
    """
    queryset = Term.objects.prefetch_related('definitions')
    serializer_class = TermSerializer



class TermSearchAPI(generics.ListAPIView):
    """
    Retrieve all Terms
    """
    queryset = Term.objects.prefetch_related('definitions')
    serializer_class = TermSerializer

    def get_queryset(self):
        """
        filtering by a term name search
        """
        search = self.kwargs['query']
        return Term.objects.prefetch_related('definitions').filter(name__icontains=search)
