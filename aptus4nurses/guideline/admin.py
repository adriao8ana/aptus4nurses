from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Patient, Symptom, MSAS, Occurrence, Treatment, Feedback, Suitability

# Register your models here.
#para poder dar export
'''
class NurseResource(resources.ModelResource):
    class Meta:
        model = Nurse
        fields = ('username', 'name', 'password')  # Specify the fields to export'''

class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient
        fields = ('patientID', 'name', 'age', 'birthday', 'contact', 'diagnosis')  # Specify the fields to export

class MSASResource(resources.ModelResource):
    class Meta:
        model = MSAS
        fields = ('occurrence', 'symptom', 'validation', 'frequency', 'severity', 'discomfort')  # Specify the fields to export

class SymptomResource(resources.ModelResource):
    class Meta:
        model = Symptom
        fields = ('symptomID', 'name', 'description')  # Specify the fields to export

class OccurrenceResource(resources.ModelResource):
    class Meta:
        model = Occurrence
        fields = ('occurrenceID', 'date_time', 'patient', 'choosenTreatments', 'suitability',   'comments')  # Specify the fields to export
        
class TreatmentResource(resources.ModelResource):
    class Meta:
        model = Treatment
        fields = ('category', 'name', 'symptoms')  # Specify the fields to export

class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Treatment
        fields = ('feedbackID', 'occurrence', 'symptom','validation', 'frequency', 'severity', 'discomfort')  # Specify the fields to export

class SuitabilityResource(resources.ModelResource):
    class Meta:
        model = Treatment
        fields = ( 'rating_1', 'rating_2','rating_3', 'rating_4')  # Specify the fields to export

#para aparecer como tabela
'''
class NurseAdmin(ImportExportModelAdmin):
    list_display = ('username', 'name', 'password')
    resource_class = NurseResource'''

class PatientAdmin(ImportExportModelAdmin):
    list_display = ('patientID', 'name', 'age', 'birthday', 'contact', 'diagnosis')
    resource_class = PatientResource

class MSASAdmin(ImportExportModelAdmin):
    list_display = ('occurrence', 'symptom', 'validation', 'frequency', 'severity', 'discomfort')
    resource_class = MSASResource
    
class SymptomAdmin(ImportExportModelAdmin):
    list_display = ('symptomID', 'name', 'description')
    resource_class = SymptomResource
   
class OccurrenceAdmin(ImportExportModelAdmin):
    list_display = ('occurrenceID', 'date_time', 'patient', 'display_choosen_treatments', 'suitability', 'comments')
    filter_horizontal = ('choosenTreatments',)
    resource_class = OccurrenceResource

    def display_choosen_treatments(self, obj):
        return ", ".join([str(treatment) for treatment in obj.choosenTreatments.all()])
    display_choosen_treatments.short_description = 'Choosen Treatments'
    
class TreatmentAdmin(ImportExportModelAdmin):
    list_display = ('category', 'name')
    filter_horizontal = ('symptoms',)
    resource_class = TreatmentResource

class FeedbackAdmin(ImportExportModelAdmin):
    list_display = ('feedbackID', 'occurrence', 'symptom','validation', 'frequency', 'severity', 'discomfort')
    resource_class = FeedbackResource
    
class SuitabilityAdmin(ImportExportModelAdmin):
    list_display = ('rating_1', 'rating_2', 'rating_3', 'rating_4')
    resource_class = SuitabilityResource

admin.site.register(Patient, PatientAdmin)
admin.site.register(Symptom, SymptomAdmin)
admin.site.register(MSAS, MSASAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Suitability, SuitabilityAdmin)
#admin.site.register(Nurse, NurseAdmin)

