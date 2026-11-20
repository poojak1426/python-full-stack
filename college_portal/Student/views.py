from django.shortcuts import render,redirect
from  django.http import HttpResponse
from .models import Student_table
from .forms import Student_form_data
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    data={
        'name':"pooja",
        'age':20,
        'department':"BCA"
    }
    marks=[100,40,50]
    return render(request,'home.html',{'data':data,'marks':marks})
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')

def forms(request):
    if request.method=="POST":
        reg_no=request.POST.get('req_no')
        name=request.POST.get('name')
        email=request.POST.get('email')
        marks=request.POST.get('marks')
        dob=request.POST.get('dob')
        Student_table.objects.create(reg_no=reg_no,name=name,email=email,marks=marks,dob=dob)
        return HttpResponse("saved successfully")
    return render(request,'Student_form.html')
def Student_form_dj(request):
    if request.method=="POST":
        form=Student_form_data(request.POST)
        if form.is_valid():
            reg_no1=form.cleaned_data['reg_no1']
            name1=form.cleaned_data['name1']
            email1=form.cleaned_data['email1']
            return HttpResponse("Saved Successfully")
        else:
            return HttpResponse("Invalid Data")
    else: 
        form=Student_form_data()  
        return render(request,'Student_form_data.html',{'form':form})
def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid username or password")
    return render(request,'login.html')
@login_required(login_url='login')
def dashboard(request):
    return render(request,'dashboard.html')
def user_logout(request):
    if request.method=='POST':
        logout(request)
        return HttpResponse("you have loged out sucessfully!")
    return HttpResponse("Invalid request")

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Student_table
from .serializers import Studentserializer


@api_view(['GET', 'POST'])
def Student_api(request):

    # GET method - Fetch all students
    if request.method == 'GET':
        students = Student_table.objects.all()
        serializers = Studentserializer(students, many=True)

        return Response(
            serializers.data,
            status=status.HTTP_200_OK
        )

    # POST method - Create a new student
    elif request.method == 'POST':
        serializers = Studentserializer(data=request.data)

        if serializers.is_valid():
            serializers.save()

            return Response(
                serializers.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializers.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
