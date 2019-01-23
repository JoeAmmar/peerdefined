from django.contrib import admin
from reversion.admin import VersionAdmin
from definitions.models import Definition
from terms.models import Term
from definitions.models import Authors

class AuthorsInLine(admin.TabularInline):
    model = Authors

@admin.register(Definition)
class YourModelAdmin(VersionAdmin):
    inlines = [AuthorsInLine,]
    pass

@admin.register(Authors)
class YourModelAdminAuthor(VersionAdmin):
    pass
