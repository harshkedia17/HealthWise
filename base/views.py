from django.shortcuts import redirect, render
from accounts.models import Doctor,Feedback
from features.models import Appointment
import pickle
import numpy as np
def home(request):
    docs = Doctor.objects.all()
    feedback = Feedback.objects.all()[:5]
    return render(request,'index.html',{'docs':docs,'feedbacks':feedback})


def appointment(request):
    if request.method == 'POST':
        # doc = Doctor.objects.filter(slug=doctor)
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']  
        date = request.POST['date']
        time = request.POST['time']
        area = request.POST['area']
        city = request.POST['city']
        new_appoint = Appointment(user=request.user,name=name,number=phone,email=email,date=date,time=time,area=area,city=city)
        new_appoint.save()
        return render(request,'account/confirm.html',{'id':new_appoint.id})
    else:
        return render(request,'account/appointment.html')
        
        
def predict(request):
    symp=['abdominal_pain', 'abnormal_menstruation', 'acidity',
       'acute_liver_failure', 'altered_sensorium', 'anxiety', 'back_pain',
       'belly_pain', 'blackheads', 'bladder_discomfort', 'blister',
       'blood_in_sputum', 'bloody_stool', 'blurred_and_distorted_vision',
       'breathlessness', 'brittle_nails', 'bruising',
       'burning_micturition', 'chest_pain', 'chills', 'coma',
       'congestion', 'constipation', 'continuous_feel_of_urine',
       'continuous_sneezing', 'cough', 'cramps', 'dark_urine',
       'dehydration', 'depression', 'diarrhoea', 'distention_of_abdomen',
       'dizziness', 'drying_and_tingling_lips', 'enlarged_thyroid',
       'excessive_hunger', 'extra_marital_contacts', 'family_history',
       'fast_heart_rate', 'fatigue', 'fluid_overload', 'headache',
       'high_fever', 'hip_joint_pain', 'history_of_alcohol_consumption',
       'increased_appetite', 'indigestion', 'inflammatory_nails',
       'internal_itching', 'irregular_sugar_level', 'irritability',
       'irritation_in_anus', 'itching', 'joint_pain', 'knee_pain',
       'lack_of_concentration', 'lethargy', 'loss_of_appetite',
       'loss_of_balance', 'loss_of_smell', 'malaise', 'mild_fever',
       'mood_swings', 'movement_stiffness', 'mucoid_sputum',
       'muscle_pain', 'muscle_wasting', 'muscle_weakness', 'nausea',
       'neck_pain', 'nodal_skin_eruptions', 'obesity',
       'pain_behind_the_eyes', 'pain_during_bowel_movements',
       'pain_in_anal_region', 'painful_walking', 'palpitations',
       'passage_of_gases', 'patches_in_throat', 'phlegm', 'polyuria',
       'prominent_veins_on_calf', 'puffy_face_and_eyes',
       'pus_filled_pimples', 'receiving_blood_transfusion',
       'receiving_unsterile_injections', 'red_sore_around_nose',
       'red_spots_over_body', 'redness_of_eyes', 'restlessness',
       'runny_nose', 'rusty_sputum', 'shivering', 'silver_like_dusting',
       'sinus_pressure', 'skin_peeling', 'skin_rash', 'slurred_speech',
       'small_dents_in_nails', 'spinning_movements', 'spotting_urination',
       'stiff_neck', 'stomach_bleeding', 'stomach_pain', 'sunken_eyes',
       'sweating', 'swelled_lymph_nodes', 'swelling_joints',
       'swelling_of_stomach', 'swollen_blood_vessels', 'swollen_legs',
       'throat_irritation', 'ulcers_on_tongue', 'unsteadiness',
       'visual_disturbances', 'vomiting', 'watering_from_eyes',
       'weakness_in_limbs', 'weakness_of_one_body_side', 'weight_gain',
       'weight_loss', 'yellow_crust_ooze', 'yellow_urine',
       'yellowing_of_eyes', 'yellowish_skin']
    # current_dir = os.path.abspath(__file__)
    # model_path = os.path.join(current_dir, 'model.pkl')
    with open("C:\\Users\\Harsh\\Desktop\\HealthWise\\health-predic\\base\\model.pkl", 'rb') as f:
        model = pickle.load(f)
    lst=[]
    answer = ' '
    
    # ypred = None
    if request.method=='POST':
        if request.POST.get('symptoms'):
            a = request.POST.get('symptoms')
            ls = a.split(',')
            for i in symp:
                if i in ls:
                    lst.append(1)
                else:
                    lst.append(0)
            inp=np.array(lst)
            y_pred = model.predict([inp])
            # print(y_pred)
            for a in y_pred:
                answer+=a
            return render(request,'predict.html',{'result':answer})
    else:
        return render(request,'predict.html',{'result':answer})
        