from django import template

register = template.Library()

@register.filter
def hours(runtime):
    return runtime // 60

@register.filter
def minutes(runtime):
    return runtime % 60
