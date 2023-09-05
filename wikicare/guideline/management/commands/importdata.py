#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:19:08 2023

@author: anagoncalves
"""

import openpyxl
from django.core.management.base import BaseCommand
from guideline.models import Treatment, Symptom
import pandas as pd
import re

#o comando é: python manage.py importdata /Users/anagoncalves/Documents/TESE/venv_wiki/wikicare/kwekke.xlsx

class Command(BaseCommand):
    help = 'Import data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        df = pd.read_excel(file_path)
        
        column_names = df.columns.tolist()

        #print(column_names)
        
        column_names_ = df.iloc[0]  # Get the first row as the category
        
        #category_row = df.iloc[0]  # Get the first row as the category
        treatment_row = df.iloc[1]  # Get the second row as the treatment names

        # Process the data and save it to the database
        # You'll need to customize this part based on your Django models and database schema
        
        for column_index, (column_name, column_data) in enumerate(df.iteritems()):
            #print(column_names)
            
            for row_index, cell_value in column_data.items():
                #print(row_index)
                symptom_name = df.iloc[row_index, 0]
                treatment_name = df.iloc[0, column_index]
                if cell_value == 'x':
                    
                    #treatment_exists = Treatment.objects.filter(name=treatment).exists()
                    print('treatment name = ', treatment_name)
                    print('category = ', column_name)
                    
                    column_name = re.sub(r'\.\d+', '', column_name)
                    treatment_instance, created = Treatment.objects.get_or_create(name=treatment_name)
                    treatment_instance.category = column_name
                    treatment_instance.save()
                    
                    # Retrieve the symptom instance based on its name
                    symptom_instance = Symptom.objects.get(name=symptom_name)
                    
                    # Assign the symptom to the treatment
                    treatment_instance.symptoms.add(symptom_instance)
                    
        #print(column_names)
        # Access the row data using row['column_name']
        # Create or update your Django model instances based on the row data
        # Save the model instances to the database
        pass

    
 