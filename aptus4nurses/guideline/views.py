from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from datetime import datetime


from django.http import HttpResponse
from .models import Patient, Symptom, MSAS, Occurrence, Treatment, Feedback, Suitability
from .forms import PatientForm, ValidationForm, MSASForm, RemainingFieldsForm, SuitabilityForm

#from .forms import PatientSearchForm
# Create your views here.


def index(request):
    return render(request, 'aptus4nurses/index.html') 

def index_patient(request):
    """View of the page to search patients"""
    patients = Patient.objects.all()
    patients_count = Patient.objects.count()
    context = {
        'patients_count': patients_count,
        'patients': patients}
    return render(request, 'aptus4nurses/search_patient.html', context)

def patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    html = render_to_string('aptus4nurses/patient.html', {'patient': patient})
    return HttpResponse(html)

def sys_guide(request):
    selected_symptoms = Symptom.objects.all()
    treatments = Treatment.objects.all()
    
    # Getting the common treatments for all symptoms
    common_treatments = get_common_treatments(selected_symptoms)
    
    treatment_data = [(item[0].name, item[1], item[2]) for item in common_treatments]
    
    str_selected_symptoms = [symptom.name for symptom in selected_symptoms]
    #request.session['common_treatments'] = treatment_data
    
    #request.session['common_treatments'] = json.dumps(common_treatments)
    request.session['selected_symptoms'] = str_selected_symptoms
    
    #separar as tabelas por tipo de tratamento
    inter_farma = []
    inter_comple = []
    inter_psico = []
    inter_fisi = []
    sup_nutri = []
    
    for item in common_treatments:
        treat = item[0]
        if treat.category == 'Intervenções farmacológica':
            inter_farma.append(item)
            
        elif treat.category == 'Estratégias Complementares':
            inter_comple.append(item)
            
        elif treat.category == 'Intervençõees psicológicas':
            inter_psico.append(item)
            
        elif treat.category == 'Intervenções físicas':
            inter_fisi.append(item)
            
        else: #suplementos nutricioanis
            sup_nutri.append(item)
        
    table_farma = generate_table(treatments, selected_symptoms, inter_farma)
    table_comple = generate_table(treatments, selected_symptoms, inter_comple)
    table_psico = generate_table(treatments, selected_symptoms, inter_psico)
    table_fisi = generate_table(treatments, selected_symptoms, inter_fisi)

    table_nutri = generate_table(treatments, selected_symptoms, sup_nutri)
   
    n_symptoms = len(selected_symptoms)
    symptom_range = range(n_symptoms)

    context = {
        'common_treatments': common_treatments,
        'symptoms': selected_symptoms,
        'treatments': treatments,
        'table_farma': table_farma,
        'table_comple': table_comple,
        'table_psico': table_psico,
        'table_fisi': table_fisi,
        'table_nutri': table_nutri,
        'n_symptoms': symptom_range  
    }

    return render(request, 'aptus4nurses/sys_guide.html', context)


def search_patient(request):
    patient_id = request.GET.get('patient_id')
    
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
            # Store patientID in the session
            request.session['patient_id'] = patient.patientID
            html = render_to_string('aptus4nurses/patient.html', {'patient': patient})
            return HttpResponse(html)
        except Patient.DoesNotExist:
            # Handle the case when the selected patient is not found
            # Return an appropriate message or redirect to an error page
            pass

    # Handle the case when no patient is selected or an error occurs
    patients = Patient.objects.all()
    return render(request, 'aptus4nurses/choose_patient.html', {'patients': patients})

def new_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_patient_success')
        else:
            # Print form validation errors for debugging purposes
            print(form.errors)
    else:
        form = PatientForm()

    return render(request, 'aptus4nurses/new_patient.html', {'form': form})

def new_patient_success(request):
    return render(request, 'aptus4nurses/new_patient_success.html')

def symptom_rating(request, step=0):
    current_datetime = datetime.now()
    patient_id = request.session.get('patient_id')
    patient_ = Patient.objects.get(patientID=patient_id)
    
    occurrence = Occurrence.objects.create(date_time=current_datetime, patient = patient_)

    request.session['occurrence_id'] = occurrence.occurrenceID
    
    request.session['feedback_validation'] = False
    request.session['edit_validation'] = False

    return redirect('symptom_rating_function', step=0)

msas_instance_list = []

def validation_view(request):
    if request.method == 'POST':
        form = ValidationForm(request.POST)
        if form.is_valid():
            request.session['validation_data'] = form.cleaned_data
            return redirect('remaining_fields')
    else:
        form = ValidationForm()
    
    return render(request, 'validation_form.html', {'form': form})

def symptom_rating_function(request, step=0):
    symptoms = Symptom.objects.all().order_by('symptomID')
    num_symptoms = symptoms.count()

    occurrence_id = request.session.get('occurrence_id')
    occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)

    str_symptom = str(symptoms[step])
    symptom_name = symptoms[step].name
    
    patient_name = occurrence.patient.name

    if request.method == 'POST':
        form = ValidationForm(request.POST)
        if form.is_valid():
            validation_data = form.cleaned_data
            
            if (validation_data['validation'] == 'True'): #tem de dar rating nos sintomas
                request.session['step'] = step
                request.session['str_ symptom'] = symptoms[step].name
                request.session['occurrence_id'] = occurrence.occurrenceID
                
                return redirect('form2_view')
                
            msas_instance = form.save(commit=False)
            msas_instance.symptom = symptoms[step]
            msas_instance.occurrence = occurrence

            next_step = step + 1
            if next_step < num_symptoms:
                msas_instance_list.append(msas_instance)
                return redirect('symptom_rating_function', step=next_step)
            else:
                msas_instance_list.append(msas_instance)
                context = {
                    'msas_instance_list': msas_instance_list,
                    'confirm_save': True,
                    'patient_name': patient_name
                    }
                return render(request, 'aptus4nurses/preview_rating.html', context)
                #return redirect('preview_rating', msas_instance_list)  # Redirect to the preview page

        else:
            print(form.errors)
    else:
        initial_data = {'symptom': symptoms[int(step)]} if int(step) < num_symptoms else {}
        form = ValidationForm(initial=initial_data)

    context = {
        'form': form,
        'step': int(step),
        'num_symptoms': num_symptoms,
        'symptom_name': symptom_name,
        'symptom': str_symptom,
        'next_step': step + 1,  # Pass the next step value to the template
        'patient_name': patient_name,
        'form_name': 'ValidationForm'
    }

    return render(request, 'aptus4nurses/symptom_rating.html', context)

def form2_view(request):
    step = request.session.get('step')
    
    str_symptom = request.session.get('str_ symptom')
    symptom = Symptom.objects.get(name=str_symptom)
    
    occurrenceID = request.session.get('occurrence_id')
    occurrence = Occurrence.objects.get(occurrenceID = occurrenceID)
    
    patient_name = occurrence.patient.name
    
    symptoms = Symptom.objects.all()
    num_symptoms = symptoms.count()
    
    if request.method == 'POST':
        form = RemainingFieldsForm(request.POST)
        if form.is_valid():
            msas_instance = form.save(commit=False)
            msas_instance.validation = True
            msas_instance.symptom = symptom
            msas_instance.occurrence = occurrence
            
            next_step = step + 1
            if request.session.get('feedback_validation'):
                num_symptoms = request.session.get('num_symptoms_feedback')
                
            if request.session.get('edit_validation'):
                # Create an instance of the MSAS model without saving it to the database yet

                symptom_id = request.session.get('symptom_id')
                msas_instance_list.insert(int(symptom_id)-1, msas_instance)

                context = {
                    'form': form,
                    'num_symptoms': num_symptoms,
                    # 'symptom': str_symptom,
                    'msas_instance_list': msas_instance_list,
                    'confirm_save': True,  # Add a flag to indicate confirmation step
                    'patient_name': patient_name
                }
                return render(request, 'aptus4nurses/preview_rating.html', context)
                
                
            if next_step < num_symptoms:
                msas_instance_list.append(msas_instance)
                if request.session.get('feedback_validation'):
                    return redirect('feedback_rating_function', step=next_step)
                else:
                    return redirect('symptom_rating_function', step=next_step)
            else:
                msas_instance_list.append(msas_instance)
                context = {
                    'msas_instance_list': msas_instance_list,
                    'confirm_save': True,
                    'patient_name': patient_name
                    }
                return render(request, 'aptus4nurses/preview_rating.html', context)
    else:
        form = RemainingFieldsForm()
    
    context = {
        'form': form,
        'step': int(step),
        'form_name': 'RemainingFieldsForm',
        'patient_name': patient_name,
        'symptom_name': str_symptom
    }
    return render(request, 'aptus4nurses/symptom_rating.html', context)    
    
def edit_rating(request, symptom_id):
    request.session['edit_validation'] = True
    position = 0
    
    for instance in msas_instance_list:

        if str(instance.symptom) == str(symptom_id):
            msas_instance_list.remove(instance)
        position += 1

    symptoms = Symptom.objects.all().order_by('symptomID')
    symptom = Symptom.objects.get(symptomID=symptom_id)
    request.session['str_ symptom'] = symptom.name
    num_symptoms = symptoms.count()

    occurrence_id = request.session.get('occurrence_id')
    occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)
    
    patient_name = occurrence.patient.name
    #occurrence.patient = patient

    if request.method == 'POST':
        form = ValidationForm(request.POST)
        if form.is_valid():
            validation_data = form.cleaned_data
            
            if (validation_data['validation'] == 'True'): #tem de dar rating nos sintomas

                request.session['symptom_id'] = symptom_id
                request.session['occurrence_id'] = occurrence.occurrenceID
                
                return redirect('form2_view')
            
            
            # Create an instance of the MSAS model without saving it to the database yet
            msas_instance = form.save(commit=False)

            msas_instance.symptom = symptom
            msas_instance.occurrence = occurrence

            msas_instance_list.insert(int(symptom_id)-1, msas_instance)

            context = {
                'form': form,
                'num_symptoms': num_symptoms,
                # 'symptom': str_symptom,
                'msas_instance_list': msas_instance_list,
                'confirm_save': True  # Add a flag to indicate confirmation step
            }
            return render(request, 'aptus4nurses/preview_rating.html', context)
        else:
            print(form.errors)

    initial_data = {'symptom': symptom}
    form = ValidationForm(initial=initial_data)
    context = {
        'form': form,
        'step': 1,
        'num_symptoms': 2,
        'symptom': symptom,
        'symptom_name': str(symptom.name),
        'msas_instance_list': msas_instance_list,
        'confirm_save': True,  # Add a flag to indicate confirmation step
        'edit': True,
        'form_name': 'ValidationForm',
        'patient_name': patient_name,
    }
    return render(request, 'aptus4nurses/symptom_rating.html', context)

def save_rating_success(request):
    nurse_id = request.session.get('nurse_id')
    #nurse = Nurse.objects.get(nurseID=nurse_id)
    if request.method == 'POST':
        feedback_validation = request.session.get('feedback_validation')
        
        if feedback_validation:      #if true, se for dar feedback a episódios anteriores
            occurrence_id = request.session.get('occurrence_id')
            occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)
            
            for instance in msas_instance_list:
                feedback = Feedback()
                #feedback.nurse = nurse
                feedback.occurrence = occurrence
                feedback.symptom = instance.symptom
                feedback.validation = instance.validation
                feedback.frequency = instance.frequency
                feedback.severity = instance.severity
                feedback.discomfort = instance.discomfort
                
                feedback.save()
            
            # Clearing the msas_instance_list
            msas_instance_list.clear()
                
            return render(request, 'aptus4nurses/feedback_success.html')
        
        else:                           #se for registar novos sintomas 
            selected_symptoms = []
            
            for instance in msas_instance_list:
                #instance.nurse = nurse
                instance.save()  # Saves the occurrence with all the symptoms to the database´´
                if instance.validation: # se o sintoma estiver positivo
                    selected_symptoms.append(instance.symptom)
                
                # Rest of the code to save symptoms
            
            #código para dar display de tratamentos possíveis
            patient_id = request.session.get('patient_id')
            patient = Patient.objects.get(patientID=patient_id)
            treatments = Treatment.objects.all()
  
            # Getting the common treatments for selected symptoms
            common_treatments = get_common_treatments(selected_symptoms)
            
            treatment_data = [(item[0].name, item[1], item[2]) for item in common_treatments]
            
            str_selected_symptoms = [symptom.name for symptom in selected_symptoms]
            request.session['common_treatments'] = treatment_data
            
            #request.session['common_treatments'] = json.dumps(common_treatments)
            request.session['selected_symptoms'] = str_selected_symptoms
            
            #separar as tabelas por tipo de tratamento
            
            inter_farma = []
            inter_comple = []
            inter_psico = []
            inter_fisi = []
            sup_nutri = []
            
            for item in common_treatments:
                treat = item[0]
                if treat.category == 'Intervenções farmacológica':
                    inter_farma.append(item)
                    
                elif treat.category == 'Estratégias Complementares':
                    inter_comple.append(item)
                    
                elif treat.category == 'Intervençõees psicológicas':
                    inter_psico.append(item)
                    
                elif treat.category == 'Intervenções físicas':
                    inter_fisi.append(item)
                    
                else: #suplementos nutricioanis
                    sup_nutri.append(item)
                
            table_farma = generate_table(treatments, selected_symptoms, inter_farma)
            table_comple = generate_table(treatments, selected_symptoms, inter_comple)
            table_psico = generate_table(treatments, selected_symptoms, inter_psico)
            table_fisi = generate_table(treatments, selected_symptoms, inter_fisi)
            table_nutri = generate_table(treatments, selected_symptoms, sup_nutri)
            
            if (len(inter_farma) != 0):
                bol_farma = True
            else:
                bol_farma = False
                
            if (len(inter_comple) != 0):
                bol_comple = True
            else:
                bol_comple = False
                
            if (len(inter_psico) != 0):
                bol_psico = True
            else:
                bol_psico = False
                
            if (len(inter_fisi) != 0):
                bol_fisi = True
            else:
                bol_fisi = False
                
            if (len(sup_nutri) != 0):
                bol_nutri = True
            else:
                bol_nutri = False
                
                
            
            #return redirect('chooseTreat')
            
            
            n_symptoms = len(selected_symptoms)
            symptom_range = range(n_symptoms)
  
            context = {
                'common_treatments': common_treatments,
                'symptoms': selected_symptoms,
                'treatments': treatments,
                'table_farma': table_farma,
                'table_comple': table_comple,
                'table_psico': table_psico,
                'table_fisi': table_fisi,
                'table_nutri': table_nutri,
                'n_symptoms': symptom_range,
                'patient': patient,
                'bol_farma': bol_farma,
                'bol_comple': bol_comple,
                'bol_psico': bol_psico,
                'bol_fisi': bol_fisi,
                'bol_nutri': bol_nutri,
                
            }
             
            return render(request, 'aptus4nurses/choose_treatment.html', context)
    
    else:
        return redirect('error')
'''
def choose_sorting(request):
    if request.method == 'POST':
        sorting_option = request.POST.get('sorting_option')  # Get the selected sorting option
        
        treatment_data = request.session.get('common_treatments', [])
        
        common_treatments = [(Treatment.objects.get(name=item[0]), item[1], item[2]) for item in treatment_data]
        
        str_selected_symptoms = request.session.get('selected_symptoms')
        selected_symptoms = [(Symptom.objects.get(name=item)) for item in str_selected_symptoms]
        
        treatments = Treatment.objects.all()
        #treatments = Treatment.objects.filter(symptoms__in=selected_symptoms).distinct()
          
        # Sorting the treatments based on the number of symptoms in common
        sorting_option = request.POST.get('sorting', 'all')
        if sorting_option == 'common':
            common_treatments = sorted(common_treatments, key=lambda item: len(item[2]), reverse=True)
        elif sorting_option == 'few':
            common_treatments = sorted(common_treatments, key=lambda item: len(item[2]))
        elif sorting_option == 'many':
            common_treatments = sorted(common_treatments, key=lambda item: len(item[2]), reverse=True)
        
        table = generate_table(treatments, selected_symptoms, common_treatments)
        


        n_symptoms = len(selected_symptoms)
        symptom_range = range(n_symptoms)
        
        # Perform sorting logic based on the selected option
        # Update the context with the sorted data
        
        context = {
            'common_treatments': common_treatments,
            'symptoms': selected_symptoms,
            'treatments': treatments,
            'table': table,
            'n_symptoms': symptom_range
        }
        
        return render(request, 'aptus4nurses/choose_treatment.html', context)  # Render the sorted table view
    
    else:
        return redirect('error')  # Redirect to an error page if the request method is not POST '''

def save_selected_treatments(request):

    if request.method == 'POST':
        selected_treatments = request.POST.getlist('symptoms')
        request.session['str_selected_treatment'] = selected_treatments
        
        occurrence_id = request.session.get('occurrence_id')
    
        str_selected_symptoms = request.session.get('selected_symptoms')
        selected_symptoms = [(Symptom.objects.get(name=item)) for item in str_selected_symptoms]
        
        occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)
        
        #treatment = Treatment.objects.get(name=selected_treatment_id)
        
        msas_instance_list.clear()
        
        context = {
            #'choosen_treatment': treatment,
            'patient': occurrence.patient,
            'symptoms': selected_symptoms
            }
        
        return render(request, 'aptus4nurses/save_treatment_success.html', context)  # Redirect to a success page after saving the treatment
    else:
        return redirect('error')  # Redirect to an error page if the request method is not POST
    
def save_commentaries(request):
    if request.method == 'POST':
        commentaries = request.POST.get('commentaries')
        request.session['commentaries'] = commentaries
        
        return redirect('treatment_suitability')  # Replace 'success_page' with the appropriate URL name for your success page
    
    # If the request method is not POST, handle it accordingly (e.g., render an error page)
    return render(request, 'error.html')

def patient_history(request):
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(patientID=patient_id)
    
    occurrences = list(Occurrence.objects.filter(patient__patientID=patient_id))
    
    msas_list = []
    for occurrence in occurrences:
        msas_list.append(list(MSAS.objects.filter(occurrence__occurrenceID = occurrence.occurrenceID)))
        
    occurrences.reverse()
        
    context = {
        'occurrences': occurrences,
        'msas_list': msas_list,
        'patient': patient
    }
    return render(request, 'aptus4nurses/patient_history.html', context)

def feedback_page(request, occurrence_id, step = 0):
    request.session['feedback_validation'] = True
    request.session['occurrence_id'] = occurrence_id
    
    # Retrieve the occurrence details based on the occurrence_id if needed
    # ...
    
    symptoms = Symptom.objects.all().order_by('symptomID')
    num_symptoms = symptoms.count()


    occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)

    str_symptom = str(symptoms[step])
    symptom_name = symptoms[step].name
    
    initial_data = {'symptom': symptoms[int(step)]} if int(step) < num_symptoms else {}
    form = MSASForm(initial=initial_data)
    
    context = {
        'form': form, 
        'step': int(step), 
        'num_symptoms': num_symptoms, 
        'symptom_name': symptom_name,
        'symptom': str_symptom,
        'occurrence_id': occurrence_id
        }
    return redirect('feedback_rating_function', step = 0)

def feedback_rating_function(request, step):
    symptoms = Symptom.objects.all().order_by('symptomID')
    
    
    occurrence_id = request.session.get('occurrence_id')
    occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)
    patient_name = occurrence.patient.name
    
    if request.method == 'POST':
        form = ValidationForm(request.POST)
        if form.is_valid():
            validation_data = form.cleaned_data
            num_symptoms = request.session.get('num_symptoms_feedback')
            symptoms_to_rate_id = request.session.get('symptoms_to_rate_id')
            
            symptom = Symptom.objects.get(symptomID=symptoms_to_rate_id[step]) #para ir buscar o correto
            
            if (validation_data['validation'] == 'True'): #tem de dar rating nos sintomas              
                request.session['step'] = step
                request.session['str_ symptom'] = symptom.name
                request.session['occurrence_id'] = occurrence.occurrenceID
                
                return redirect('form2_view')
                
            msas_instance = form.save(commit=False)
            
            msas_instance.symptom = symptom
            msas_instance.occurrence = occurrence

            next_step = step + 1
        
            if next_step < num_symptoms:
                msas_instance_list.append(msas_instance)
                return redirect('feedback_rating_function', step=next_step)
            else:
                
                msas_instance_list.append(msas_instance)
                
                context = {
                    'msas_instance_list': msas_instance_list,
                    'confirm_save': True,
                    'patient_name': patient_name
                    
                    }
                return render(request, 'aptus4nurses/preview_rating.html', context)
                #return redirect('preview_rating', msas_instance_list)  # Redirect to the preview page

        else:
            print(form.errors)
        
    else:
        msas_instances = MSAS.objects.filter(occurrence = occurrence)
        symptoms_to_rate = []
        symptoms_to_rate_id = []
        for msas in msas_instances: 
            if msas.validation == True:    # os symptoms que têm rating para dar
                symptoms_to_rate.append(msas)
                symptoms_to_rate_id.append(msas.symptom.symptomID)
                
        num_symptoms = len(symptoms_to_rate)  
        request.session['num_symptoms_feedback'] = num_symptoms
        
        request.session['symptoms_to_rate_id'] = symptoms_to_rate_id
        
        initial_data = {'symptom': symptoms_to_rate[step]}

        #initial_data = {f'symptom': item for  item in enumerate(symptoms_to_rate, start=1)}
        #initial_data = {'symptom': symptom for symptom in symptom_to_rate}
        form = ValidationForm(initial = initial_data)


    context = {
        'form': form,
        'step': int(step),
        'num_symptoms': num_symptoms,
        'symptom_name': symptoms_to_rate[step].symptom.name,
        'patient_name': patient_name,
        #'symptom': str_symptom,
        'next_step': step + 1,  # Pass the next step value to the template
        'form_name': 'ValidationForm'
    }

    return render(request, 'aptus4nurses/symptom_rating.html', context)

def treatment_suitability(request):
    occurrence_id = request.session.get('occurrence_id')
    occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)
   
    
    
    if request.method == 'POST':     
        form = SuitabilityForm(request.POST)
        if form.is_valid():
            
            rating_1 = form.cleaned_data['rating_1']
            rating_2 = form.cleaned_data['rating_2']
            rating_3 = form.cleaned_data['rating_3']
            rating_4 = form.cleaned_data['rating_4']
            
            
            '''
            aim_rating = form.cleaned_data['aim']
            iam_rating = form.cleaned_data['iam']
            fim_rating = form.cleaned_data['fim'] '''
            #suitability = form.cleaned_data['suitability']
            #request.session['suitability'] = suitability
            
            # Save the ratings to your Suitability model
            suitability = Suitability.objects.create(rating_1=rating_1, rating_2=rating_2, rating_3=rating_3, rating_4=rating_4)

            # Save suitability to the session (if needed)
            request.session['suitability'] = suitability.pk
          
            commentaries = request.session.get('commentaries')
            
            str_selected_treatment = request.session.get('str_selected_treatment')

            context = {
                'occurrence': occurrence,
                'comments': commentaries,
                'treatment': str_selected_treatment,
                'suitability': suitability
                }

            return render(request, 'aptus4nurses/suitability_success.html', context)  # Redirect to a success page or any other desired page
        else:
            print(form.errors)  # Print form errors to the console
    else:
        form = SuitabilityForm()

    context = {
        'form': form,
        'patient': occurrence.patient,
    }
    return render(request, 'aptus4nurses/suitability.html', context)

def save_final_occurrence(request):
    occurrence_id = request.session.get('occurrence_id')
    occurrence = Occurrence.objects.get(occurrenceID=occurrence_id)
    
    if request.method == 'POST':
        
        str_selected_treatment = request.session.get('str_selected_treatment')

        commentaries = request.session.get('commentaries')
        
        # Retrieve the suitability instance using the primary key stored in the session
        suitability_id = request.session.get('suitability')
        suitability = Suitability.objects.get(pk=suitability_id)
        #suitability = request.session.get('suitability')

        
        treatments = []
        
        for str_treat in str_selected_treatment:
            treatment = Treatment.objects.get(name=str_treat)
            treatments.append(treatment)
        
        occurrence.choosenTreatments.set(treatments)  # Assign the list of selected treatments to the choosenTreatments field
        
       
        #treatment = Treatment.objects.get(name=selected_treatment_id)

        
        occurrence.comments = commentaries
        occurrence.suitability = suitability
        
        occurrence.save()
        
        del request.session['str_selected_treatment']
        del request.session['commentaries']
        del request.session['suitability']
        del request.session['occurrence_id']
        
        return render(request, 'aptus4nurses/index.html')
        


def get_treatments_for_symptom(symptomID):
    symptom = Symptom.objects.get(symptomID = symptomID)
    treatment = Treatment.objects.filter(symptoms=symptom)
    return treatment

def generate_table(treatments, symptoms, common_treatments):
    table = []
    
    # Create the header row
    header_row = ['Tratamento'] + [item[0].name for item in common_treatments]
    table.append(header_row)
    
    # Iterate over each symptom
    for symptom in symptoms:
        row = [symptom.name]
        
        # Check if the symptom is associated with each treatment
        for item in common_treatments:
            treatment = item[0]
            
            if any(symptom.name in item[2] and item[0] == treatment for item in common_treatments):
                row.append('x')
            else:
                row.append('')
        
        table.append(row)
    return table
'''
def generate_table(treatments, symptoms, common_treatments):
    # Create a dictionary to store the count of occurrences of each treatment
    treatment_count = {treatment: 0 for treatment in treatments}

    # Count the occurrences of each treatment in the common treatments
    for item in common_treatments:
        treatment = item[0]
        treatment_count[treatment] += 1

    # Sort the treatments based on their occurrence in descending order
    sorted_treatments = sorted(treatment_count.items(), key=lambda x: x[1], reverse=True)

    table = []

    # Create the header row
    header_row = ['Treatments'] + [item[0].name for item in sorted_treatments]
    table.append(header_row)

    # Iterate over each symptom
    for symptom in symptoms:
        row = [symptom.name]

        # Check if the symptom is associated with each treatment
        for treatment, _ in sorted_treatments:
            if any(symptom.name in item[2] and item[0] == treatment for item in common_treatments):
                row.append('x')
            else:
                row.append('')

        table.append(row)

    return table
'''

def get_common_treatments(symptoms):
    treatments_list = []
    common_treatments = []

    for symptom in symptoms:
        treatments_per_symptom = get_treatments_for_symptom(symptom)
        for treatment in treatments_per_symptom:
            treatments_list.append(treatment)
    
    
    for treatment in treatments_list:
        number = treatments_list.count(treatment)
        
        symptom_names = [symptom.name for symptom in symptoms if treatment in get_treatments_for_symptom(symptom)]
        pair = (treatment, number, symptom_names)
        common_treatments.append(pair)

    # Remove duplicates while preserving order
    unique_list = []
    
    
    [unique_list.append(x) for x in common_treatments if x not in unique_list]


    return unique_list 

def error(request):
    return render(request, 'aptus4nurses/error.html')

def get_treatments_for_patient_symptom(patient, symptom):
    return Treatment.objects.filter(symptoms=symptom, patient=patient)


            
    
    
    
    
    
    
    
    
    
    
    
    
    