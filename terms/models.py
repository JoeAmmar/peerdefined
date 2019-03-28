from django import template
from django.contrib.auth import get_user_model # returns user model currently active in project
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import misaka #allows us to use markdown inside of posts

User = get_user_model() #allows us to get things off of current user session

register = template.Library()

class Term(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(allow_unicode = True, unique = True) #name field sluggified
    usersFollowing = models.ManyToManyField(User, blank=True,
                                            related_name='followingTerms')
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) #slugify will lowercase text (and replace whitespace)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('definitions:term_single', kwargs = {'termSlug':self.slug}) 


    class Meta():
        ordering = ['name',]

    def __str__(self):
        return self.name
