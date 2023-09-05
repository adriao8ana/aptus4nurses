#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 11:52:29 2023

@author: anagoncalves
"""

from django import template

register = template.Library()

@register.filter
def get_treatments(symptom_name, symptom_treatments):
    return symptom_treatments.get(symptom_name, [])