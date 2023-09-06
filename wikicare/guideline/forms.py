#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:35:40 2023

@author: anagoncalves
"""

from django import forms
from guideline.models import Patient, MSAS, Symptom, Occurrence, Treatment, Suitability

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'patientID', 'age', 'birthday', 'contact', 'diagnosis']
        
class ValidationForm(forms.ModelForm):
    validation = forms.TypedChoiceField(
        label='Validation',
        choices=[(True, 'Sim'), (False, 'Não')],
        widget=forms.RadioSelect(attrs={'class': 'validation-radio'})
    )
    class Meta:
        model = MSAS
        fields = ['validation']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['validation'].label = ''
    

class RemainingFieldsForm(forms.ModelForm):
    FREQUENCY_CHOICES = [
        (1, "1 - Raramente"),
        (2, "2 - Ocasionalmente"),
        (3, "3 - Frequentemente"),
        (4, "4 - Quase Constantemente")
    ]
    SEVERITY_CHOICES = [
        (1, "1 - Ligeira"),
        (2, "2 - Moderada"),
        (3, "3 - Severa"),
        (4, "4 - Muito Severa")
    ]
    DISCOMFORT_CHOICES = [
        (0, "0 - Nada"),
        (1, "1 - Um pouco"),
        (2, "2 - Bastante"),
        (3, "3 - Muito"),
        (4, "4 - Muitíssimo")
    ]
    
    frequency = forms.IntegerField(
        label='Frequência',
        widget=forms.RadioSelect(choices=FREQUENCY_CHOICES),
        required=False
    )
    severity = forms.IntegerField(
        label='Severidade',
        widget=forms.RadioSelect(choices=SEVERITY_CHOICES),
        required=False
    )
    discomfort = forms.IntegerField(
        label='Incómodo',
        widget=forms.RadioSelect(choices=DISCOMFORT_CHOICES),
        required=False
    )
    
    class Meta:
        model = MSAS
        fields = ['frequency', 'severity', 'discomfort']
        

'''
class SuitabilityForm(forms.ModelForm):
    CHOICES = [
        (0, "0 - Muito adequado"),
        (1, "1 - Adequado"),
        (2, "2 - Neutro"),
        (3, "3 - Desadequado"),
        (4, "4 - Muito desadequado")
    ]

    suitability = forms.ChoiceField(
        label='Suitability',
        choices=CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    class Meta:
        model = Occurrence
        fields = ['suitability'] 
 
        
class SuitabilityForm(forms.ModelForm):
    class Meta:
        model = Suitability
        fields = ()

    
    aim = forms.ModelChoiceField(queryset=AIM.objects.all(), widget=forms.HiddenInput())
    aim_sentence_1 = forms.CharField(widget=forms.HiddenInput())
    aim_rating_1 = forms.ChoiceField(choices=AIM.RATING_CHOICES, widget=forms.RadioSelect(), required=False)

    aim_sentence_2 = forms.CharField(widget=forms.HiddenInput())
    aim_rating_2 = forms.ChoiceField(choices=AIM.RATING_CHOICES, widget=forms.RadioSelect(), required=False)

    aim_sentence_3 = forms.CharField(widget=forms.HiddenInput())
    aim_rating_3 = forms.ChoiceField(choices=AIM.RATING_CHOICES, widget=forms.RadioSelect(), required=False)

    aim_sentence_4 = forms.CharField(widget=forms.HiddenInput())
    aim_rating_4 = forms.ChoiceField(choices=AIM.RATING_CHOICES, widget=forms.RadioSelect(), required=False)
    
    iam = forms.ModelChoiceField(queryset=IAM.objects.all(), widget=forms.RadioSelect(), empty_label=None)
    fim = forms.ModelChoiceField(queryset=FIM.objects.all(), widget=forms.RadioSelect(), empty_label=None)  '''
    
    
class SuitabilityForm(forms.ModelForm):
    class Meta:
        model = Suitability
        fields = ('rating_1', 'rating_2','rating_3', 'rating_4')
        
    
 
class MSASForm(forms.ModelForm):
    validation = forms.TypedChoiceField(
        label='Validation',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect(attrs={'class': 'validation-radio'})
    )
    frequency = forms.IntegerField(
        label='Frequency',
        min_value=1,
        max_value=4,
        required=False
    )
    severity = forms.IntegerField(
        label='Severity',
        min_value=1,
        max_value=4,
        required=False
    )
    discomfort = forms.IntegerField(
        label='discomfort',
        min_value=0,
        max_value=4,
        required=False
    )

    class Meta:
        model = MSAS
        fields = ['validation', 'frequency', 'severity', 'discomfort']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validation = self.initial.get('validation')

        if validation is not None and validation is False:
            self.fields['frequency'].widget = forms.HiddenInput()
            self.fields['severity'].widget = forms.HiddenInput()
            self.fields['discomfort'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        validation = cleaned_data.get('validation')

        if validation is not None and validation is False:
            cleaned_data['frequency'] = None
            cleaned_data['severity'] = None
            cleaned_data['discomfort'] = None

        return cleaned_data 
    


    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        