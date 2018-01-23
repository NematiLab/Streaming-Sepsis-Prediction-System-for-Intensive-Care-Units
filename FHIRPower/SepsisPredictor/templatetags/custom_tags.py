from django import template
register = template.Library()

@register.filter
def index(array, i):
    return array[int(i)]

@register.filter
def last_index(array):
    return array[len(array)]

@register.filter
def get_item(Measure):
    return Measure.patient_name
