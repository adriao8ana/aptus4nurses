#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:29:43 2023

@author: anagoncalves
"""

from django.urls import path
from django.contrib import admin
#now import the views.py file into this code

app_name = 'main'
from . import views
urlpatterns=[
  #path('', views.login_view, name = 'login'),
  path('', views.index, name = 'index'),
  path('index/', views.index, name = 'index'),
  #path('register/', views.register_nurse, name='register_nurse'),
  path('index_patient/', views.index_patient, name = 'index_patient'),
  path('search_patient/', views.search_patient, name = 'search_patient'),
  path('patient/<int:pk>/', views.patient, name='patient'),
  
  
  path('patients/new/', views.new_patient, name='new_patient'),
  path('new_patient_success/', views.new_patient_success, name = 'new_patient_success'),
  
  path('symptom_rating/<int:step>', views.symptom_rating, name='symptom_rating'),
  path('symptom_rating_function/<int:step>/', views.symptom_rating_function, name='symptom_rating_function'),
  path( 'form2/', views.form2_view, name = 'form2_view'),
  #path('save_rating/', views.save_rating, name='save_rating'),
  path('save_rating_success/', views.save_rating_success, name='save_rating_success'),
  #path('choose_sorting/', views.choose_sorting, name = 'choose_sorting'),
  path('save_selected_treatments/', views.save_selected_treatments, name='save_selected_treatments'),
  path('save_commentaries/', views.save_commentaries, name='save_commentaries'),
  path('save_final_occurrence/', views.save_final_occurrence, name='save_final_occurrence'),
  #path('provide-feedback/', views.provide_feedback, name='provide_feedback'),
  path('feedback/<int:occurrence_id>/', views.feedback_page, name ='feedback_page'),
  path('feedback_rating_function/<int:step>', views.feedback_rating_function, name ='feedback_rating_function'),
  
  path('treatment_suitability/', views.treatment_suitability, name = 'treatment_suitability'),

  #path('preview_rating/', views.preview_rating, name='preview_rating'),
  path('error/', views.error, name='error'),
  
  #path('edit_rating/', views.edit_rating, name='edit_rating'),
  path('edit_rating/<str:symptom_id>/', views.edit_rating, name='edit_rating'),
  
  path('occurrences/', views.patient_history, name='patient_history'),
  #path('recomendation/', views.recomendation, name='recomendation'),
  
  
  path('sys_guide/', views.sys_guide, name = 'sys_guide'),
  path('admin/', admin.site.urls)
]
















