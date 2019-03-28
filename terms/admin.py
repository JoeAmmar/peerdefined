from django.contrib import admin
from definitions.models import Definition
from definitions.models import Authors
from terms.models import Term
from reversion.admin import VersionAdmin
import nested_admin

class AuthorsInline(nested_admin.NestedStackedInline):
    model = Authors
    extra = 0
    inline_classes = ('grp-collapse grp-open',)

class DefinitionInLine(nested_admin.NestedStackedInline):
    model = Definition
    inlines = [AuthorsInline]
    extra = 0

@admin.register(Term)
class ourModelAdmin(VersionAdmin, nested_admin.NestedModelAdmin):
    inlines = [DefinitionInLine]
    pass
