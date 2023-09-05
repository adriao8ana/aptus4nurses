#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 15:11:00 2023

@author: anagoncalves
"""

import pandas as pd
from guideline.models import Treatment, Symptom

df = pd.read_excel(r'/Users/anagoncalves/Documents/TESE/venv_wiki/wikicare/kwekke.xlsx')


for treatment_name in df.columns:
    # Access column data using df[column_name] or df.loc[:, column_name]
    for value in df[treatment_name]:
        if value == 'x':
            print(df.loc[:, treatment_name])
            treatment = Treatment.objects.get_or_create(name=treatment_name)
            #symptom = Symptom.objects.get_or_create(name = )
            
        
































