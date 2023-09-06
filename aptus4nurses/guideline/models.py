# import the model


#De acordo com as seguintes perguntas selecione a opção que melhor se adequa ao paciente.from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db import models
import openpyxl


#create a new instacy

    

class Patient(models.Model):
    patientID = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=3)
    birthday = models.DateField()
    contact = models.CharField(max_length=20)

    # Read diagnosis options from Excel file
    diagnosis_options = []
    wb = openpyxl.load_workbook('CID-O.xlsx')
    sheet = wb.active
    
   
    for cell in sheet['A']:
        diagnosis_options.append((cell.value, cell.value))

    diagnosis = models.CharField(max_length=200, choices=diagnosis_options)

    def __str__(self):
        return self.patientID
    
class Symptom(models.Model):
    symptomID = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.symptomID
    
class Treatment(models.Model):
    category = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    symptoms = models.ManyToManyField(Symptom)
    
    def __str__(self):
        return self.name



class Suitability(models.Model):
    RATING_CHOICES = (
        ("Discordo completamente", "Discordo completamente"),
        ("Discordo", "Discordo"),
        ("Neutro", "Neutro"),
        ("Concordo", "Concordo"),
        ("Concordo completamente", "Concordo completamente"),
    )

    #suitability_id = models.AutoField(primary_key=True)  # This will add an auto-incrementing id field

    
    rating_1 = models.CharField(max_length=50, choices=RATING_CHOICES, default="Neutral")
    rating_2 = models.CharField(max_length=50, choices=RATING_CHOICES, default="Neutral")
    rating_3 = models.CharField(max_length=50, choices=RATING_CHOICES, default="Neutral")
    rating_4 = models.CharField(max_length=50, choices=RATING_CHOICES, default="Neutral")
    
   
    
class Occurrence(models.Model):
    occurrenceID = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    choosenTreatments = models.ManyToManyField(Treatment, blank=True)
    suitability = models.ForeignKey(Suitability, on_delete=models.CASCADE, null=True, blank=True)
    comments = models.TextField()
    
    # Add any other fields related to the occurrence
    
    def __str__(self):
        return f"{self.occurrenceID}"
    
class MSAS(models.Model):
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    validation = models.BooleanField(default=False)
    frequency = models.IntegerField(default=0)
    severity = models.IntegerField(default=0)
    discomfort = models.IntegerField(default=0)   

    
class Feedback(models.Model):
    feedbackID = models.AutoField(primary_key=True)
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    validation = models.BooleanField(default=False)
    frequency = models.IntegerField()
    severity = models.IntegerField()
    discomfort = models.IntegerField()
    #nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return f"{self.feedbackID}"
    