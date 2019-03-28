from django import template
import re

#Register Template Tag
register = template.Library()


# The following termplate tag is used to extract the termId and the termSlug
# the notification description sent when a definition is modified
# It's used to link to the term's definition page

@register.filter
def id_term_tag(value,arg):
    if len(str(value)) > 10:
        termId,termSlug = re.findall('.{1,10}', value)
        if arg == 'termId' or arg == "":
            return int(termId)
        else:
            return termSlug
    else:
        return value
