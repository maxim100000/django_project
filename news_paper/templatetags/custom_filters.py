from django import template

register = template.Library()

@register.filter()
def censor(value:str):
    arr = value.split(' ')
    for index, v in enumerate(arr):
        if v.startswith('с'): arr[index] = '!CENSORED!'  
    return ' '.join(arr)
    