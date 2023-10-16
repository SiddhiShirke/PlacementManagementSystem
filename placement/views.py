from datetime import date

from django.shortcuts import render
from .forms import RegisterForms,studendDataForm,companyDetailsForm,training_form
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import signup,studentData,company_details,appliedStudents,training_skill
from django.contrib.auth.decorators import user_passes_test
from django.db.utils import IntegrityError
from django.db.models import F
from django.db.utils import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import io
import base64
from collections import Counter
from django.db.models import Count
def home(request):
    print(request.user)
    return render(request,'home.html')

def register(request):
    form = RegisterForms()
    if request.method == 'POST':
        form = RegisterForms(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password')
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/studentDataForm')
    else:
        messages.error(request,"Invalid data")

    return render(request,'signup.html',{'form1':form})

@login_required(login_url="/signin")
def studentDataView(request):
    print(request.user)
    form = studendDataForm()
    if request.method=='POST':
        form =studendDataForm(request.POST)
        try:
            if form.is_valid():
                data = form.save(commit=False)
                email = request.user

                data.user = email
                data.save()

                return redirect('/studentSection')

        except IntegrityError:
            return HttpResponse("<h1></h1>")
    return  render(request,'studentForm.html',{'form':form})

@login_required(login_url="/signin")
def updateprofile(request):
    try:
        obj = get_object_or_404(studentData, user_id=request.user.id)
        form = studendDataForm(request.POST or None, request.FILES or None, instance=obj,)
        if form.is_valid():
            form.save()
            messages.success(request,"Details Updated Successfully")
        return render(request,"updateprofile.html",{'form':form})

    except:
        print("Okay")
        return HttpResponse("<h2>Fill your data first <a href='/studentDataForm'> here</a></h2>")
    
@login_required(login_url="/signin")
def studentSection(request):
    return render(request,'studentSection.html')




@login_required(login_url="/signin")
def applied(request,id):
    print(id, request.user)
    user_id = signup.objects.get(email=request.user)
    comp_id =company_details.objects.get(id=id)
    print(user_id.id)
    try:
        studata = studentData.objects.get(user=user_id)
    except ObjectDoesNotExist:
        messages.warning(request,"Complete you profile before applying for any drive! by clicking on Edit Profile")
        return redirect('/studentSection')
    print("Studata")
    print(studata)
    print(studata.skills)
    skill= studata.skills
    arr = skill.split(",")
    print("ARR")
    print(arr)
    obj=[]
    print(len(arr))

    for i in range(len(arr)):
        print(i)
        query =((company_details.objects.filter(skills_required__icontains=arr[i],id=id)))
        if query:
            obj.append(query)

    print(obj)
    print(type(obj))
    # obj1 = (company_details.objects.filter(skills_required__in=arr))
    # print(obj1)
    #cskills = comp.skills_required
    #print("cskills" + cskills)
    try :
        if obj:
            apply = appliedStudents.objects.create(user=user_id, company=comp_id)

            apply.save()
            messages.success(request,"Applied Successfully!")
            return redirect('/studentSection')
            # return render(request, 'applied.html')
        else:
            messages.warning(request,"No Matching Skills!!")
            return redirect('/studentSection')
        #,{'obj':obj1,'arr':arr}

    except IntegrityError:
        messages.warning(request,"You have already applied to this job !!!")
        return redirect('/studentSection')
        # return HttpResponse('<h2>You have already applied to this job !!!!'
        #                     '</h2><a href="/">Go Back</a> <br> <a href="/drivelistforStudent" > Check Applied</a>')

@login_required(login_url="/signin")
def appliedListForStudent(request):
    data = appliedStudents.objects.filter(user=request.user)

    return render(request,'studentapplied.html',{'data':data})

@login_required(login_url="/signin")
def profile(request):
    data = studentData.objects.get(user_id=request.user)
    #print(request.user)
    #print(data.skills)
    return render(request,"profile.html",{"data":data})

@login_required(login_url="/signin")
def showDriveList(request):
    listdata = []
    data = company_details.objects.all()
    for i in data:
        if i.last_date_of_applying > date.today():
            listdata.append(i)
    return render(request,'drivelist.html',{'data':listdata})
#Company Details
def check_admin(request):
   return request.is_superuser
@login_required(login_url="/signin")
def notadmin(request):
    return HttpResponse("<h1>You're not an Admin</h1>")
@user_passes_test(check_admin,login_url="/notadmin")
def coordinatorSection(request):
    return render(request,'coordinatorSection.html')

@user_passes_test(check_admin,login_url="/notadmin")
def company_del(request):
    form = companyDetailsForm()
    if request.method=='POST':
        form = companyDetailsForm(request.POST)
        if form.is_valid():
            # new_comp_name = request.POST['company_name']
            # already_exist_company = company_details.objects.filter(company_name=new_comp_name)
            # if already_exist_company is not null:
            #     messages.error(request,"Company is already registered!")
            #     return redirect('/coordinatorSection')
            data = form.save(commit=False)
            data.save()
            messages.success(request,"Company Detail is saved successfully !")
            return redirect('/coordinatorSection')
        else:
            messages.error(request,"Invalid Data!")
    return render(request,'companydetails.html',{'form':form})

#for Coordinator
@user_passes_test(check_admin,login_url="/notadmin")
def appliedStudentList(request):
    data = appliedStudents.objects.all()
    return render(request,'appliedStudentList.html',{'data':data})

@user_passes_test(check_admin,login_url="/notadmin")
def CompList(request):
    comp = company_details.objects.all()
    return render(request,'drivenamelist.html',{'comp':comp})
@user_passes_test(check_admin,login_url="/notadmin")
def elligibleStudents(request,id):
    list_student=[]
    comp_id=company_details.objects.get(id=id)
    print(comp_id,"Elligible")
    skills = comp_id.skills_required
    skills = skills.split(",")
    print(skills)
    for i in skills:
        print(i)
        obj =studentData.objects.filter(skills__icontains=i)
        print("Object: " , obj)
        for i in obj:
            # print("Object I : " ,i)
            list_student.append(i)

    unique_list = list(set(list_student))
    print("Student")
    # for i in obj:
    #     print(i.user)
    #     print(i.skills)
    print("Skills")
    print(skills)
    print("List OF Students ")
    for i in list_student:
        print("LIST ITEM:" ,i)
    return render(request,'shortlistedStudents.html',{'obj':unique_list,'comp_id':comp_id})

#Send Mail to Shortlisted Students
def mail_shortlistStudents(request,id,comp_id):
    comp_name=company_details.objects.get(id=comp_id)
    print(comp_name.company_name)
    print(comp_name.job_title)
    user = studentData.objects.get(id=id)
    print(user.first_name)
    subject = 'This is in regards to the placement cell'
    message = f"Hi {user.first_name} {user.last_name}, you are shortlisted  for the profile of {comp_name.job_title} which is through {comp_name.company_name} Visit the site and apply for the same."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user, ]
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse("<h1>Mail Sent Successfully</h1>")


#Raise poll
#def poll(request):


def graph(request):
    # Read external CSV data
    df = pd.read_csv(r'C:\Users\Shirke\Documents\FYMCA\placement\data.csv')
    print(df)
    column_name = 'Type of Job'  # Replace with the actual column name

    # Get value counts for the column
    value_counts = df[column_name].value_counts()

    # Create a pie chart
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
    plt.title("Placement and Internship Report")
    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()



    # Encode the image as base64

    frequent_title1 = company_details.objects.values_list('job_title').annotate(freq_val=Count('job_title')).order_by('-freq_val')
    print(frequent_title1)

    #plt.pie()
    context = {'chart_image': chart_image,'cname':frequent_title1}
    return render(request, 'pie_chart.html', context)




@login_required(login_url="/signin")
def trainingView(request):
    form=training_form()
    if request.method =="POST":
        form = training_form(request.POST)
        try:
            if form.is_valid():
                data = form.save(commit=False)
                data.user=request.user
                data.save()
                messages.success(request,"Response Recorded Successfully")
        except IntegrityError:

            messages.error(request,"You can respond only once")


    return render(request,'trainingForm.html',{'form':form})

@user_passes_test(check_admin,login_url="/notadmin")
def trainingPieChart(request):
    domain_data = training_skill.objects.all()
    domain_categories=[]
    soft_categories=[]
    for i in domain_data:
        print(i.interested_in_technical_training)
        domain_categories.append(i.interested_in_technical_training)
        soft_categories.append(i.interested_in_soft_skill_training)
    print(domain_categories, "Hee;")
    domain_count = Counter(domain_categories)
    softskill_count=Counter(soft_categories)
    print(domain_count)
    #
    # Create a pie chart using matplotlib
    labels = domain_count.keys()
    values = domain_count.values()

    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title('Domain Training Report')

    # Save the plot to a bytes object
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Encode the plot image to base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    label1 = softskill_count.keys()
    values1 = softskill_count.values()
    plt.pie(values1,labels=label1,autopct='%1.1f%%')
    plt.title("Soft Skill Training Report")
    image_stream1=io.BytesIO()
    plt.savefig(image_stream1,format='png')
    plt.close()
    softImg = base64.b64encode(image_stream1.getvalue()).decode('utf-8')
    context = {'pie_chart': image_base64,'softskillpie':softImg}
    return render(request, 'trainingChart.html',context)

#companywise data
@user_passes_test(check_admin,login_url="/notadmin")
def selectcompanyname(request):
    select = company_details.objects.all
    return render(request,'compname.html',{'select':select})

@user_passes_test(check_admin,login_url="/notadmin")
def displayCompList(request,id):
    comp_id = company_details.objects.get(id=id)
    data = appliedStudents.objects.filter(company=comp_id)
    return render(request,'displayOneCompDel.html',{'data':data})


@login_required
def user_log(request):
    return HttpResponse("Hey You're Logged in " , request.user.email)

def signin(request):
    if request.user.is_authenticated:
        return render(request,'studentSection.html')
    else:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            email = request.POST['username']
            password =request.POST['password']
            user =authenticate(request,email=email,password=password)
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect('/coordinatorSection')
                else:
                    login(request,user)
                    return redirect('/studentSection')
            else:
                messages.error(request,"Invalid Credentials!")
        else:
            form = AuthenticationForm()
    return render(request,'signin.html',{'form':form})

def logout(request):
    if request.user.is_authenticated:
        logout_auth(request)
        messages.success(request,'You logged out')
        return redirect('/signin')
    else:
        return HttpResponse("You're not logged in")