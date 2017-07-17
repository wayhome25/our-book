from django import template
import re


register = template.Library()

@register.filter
def book_title(value):
    title = value.replace('(', '<br><h5>(', 1) + '</h5>'
    return title


@register.filter
def book_pub_date(value):
    pub_date = re.sub(r'(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})', r'\g<year>.\g<month>.\g<day>', value)
    return pub_date