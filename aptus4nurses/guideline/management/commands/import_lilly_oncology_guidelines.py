#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 10:46:54 2023

@author: anagoncalves
"""

# management/commands/import_lilly_oncology_guidelines.py
from django.core.management.base import BaseCommand
from guideline.import_data import import_lilly_oncology_guidelines

class Command(BaseCommand):
    help = 'Imports Lilly Oncology Guidelines to the database'

    def handle(self, *args, **options):
        import_lilly_oncology_guidelines()
        self.stdout.write(self.style.SUCCESS('Lilly Oncology Guidelines imported successfully.'))