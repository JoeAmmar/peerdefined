from django import template
register = template.Library()

# Adapted from the following page:
# https://techstricks.com/creating-a-custom-template-tag-in-django/

@register.tag
def range(num):
    """
    Returns a list of hours in a day by 24 hour clock.
    """
    return [x in range(num)]
