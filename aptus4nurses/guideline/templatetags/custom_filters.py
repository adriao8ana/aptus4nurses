from django import template

register = template.Library()

@register.filter
def has_symptom(common_treatments, symptom, treatment):
    return any(symptom.name in item[2] and item[0] == treatment for item in common_treatments)# -*- coding: utf-8 -*-

