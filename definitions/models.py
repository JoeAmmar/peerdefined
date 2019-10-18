#import from packages
from django.conf import Settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
import reversion
import tagulous
from tagulous.models import TagField

# Import from models and other
from terms.models import Term
from definitions.discChoices import disciplineChoices



User = get_user_model()  # connects current definition to user logged in


# Used for organizing definition synonyms in a tag-like fashion
class Synonym(tagulous.models.TagModel):
    class TagMeta:
        initial = [
            'flair',
        ]
        space_delimiter = False
        autocomplete_view = 'definition_synonym_autocomplete'

# Used for organizing definition disciplines in a tag-like fashion
class Discipline(tagulous.models.TagModel):
    class TagMeta:
        initial = disciplineChoices
        space_delimiter = False
        autocomplete_view = 'definition_discipline_autocomplete'

#Definition model
class Definition(models.Model):
    user = models.ForeignKey(User,
                             related_name='definitions',
                             on_delete=models.CASCADE)
    usersFollowing = models.ManyToManyField(User, blank=True,
                                            related_name='followingDefs')
    #Original_user differs from User (the user who most recently modified a definition)
    original_user = models.ForeignKey(User,
                                      null=True,
                                      blank=True,
                                        related_name='definitions_orig',
                                         on_delete = models.CASCADE)
    # DateTime definitioned is automatically Generated
    created_at = models.DateTimeField(auto_now=True)
    # Actual definition
    defs = models.TextField()
    term = models.ForeignKey(Term,
                             related_name='definitions',
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE)
    year = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    discipline = tagulous.models.TagField(Discipline,
                                          help_text="This field splits tags on commas",
                                          blank=True)
    synonym = tagulous.models.TagField(Synonym,
                                       help_text="This field splits tags on commas",
                                       blank = True)
    # Number of citations
    citeNumber = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    class Meta:
        ordering = ['-citeNumber'] #order by citation number in descending order
        unique_together = ['user', 'defs'] # may delete later

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # absolute url for definition is in reference to its term
        return reverse('definitions:term_single', kwargs = {'termSlug':self.term.slug,})

    #  May remove the below
    def __str__(self):
        if self.author.all():
            return self.author.all()[0].in_text + " (" + self.term.name + ")"
        else:
            return "(" + self.term.name + ")"

#Authors Keeps citation information (APA style)
class Authors(models.Model):
    in_text = models.CharField(max_length=500, null=True, blank=True)
    citation = models.TextField(max_length=1200, null=True, blank=True)
    doi = models.CharField(max_length=100, null=True, blank=True)
    definitions = models.ForeignKey(Definition,
                                    related_name='author',
                                    on_delete = models.CASCADE,
                                    null = True,
                                    blank = True)
    def __str__(self):
        return self.in_text

# While the model below is not currently in use, the site may be redesigned to include it:
class Article(models.Model):
    journal = models.TextField(null=True, blank=True)
    issue = models.TextField(null=True, blank=True)
    volume = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    year = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.authors
