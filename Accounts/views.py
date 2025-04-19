from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def login(request):
    try:
        if request.method == 'POST':
            rollno=request.POST.get('roll')
            pass1=request.POST.get('password')

            user=auth.authenticate(username=rollno,password=pass1)

            if user is not None:
                auth.login(request,user)
                return redirect('/')
            else:
                messages.info(request,'Invalid Username or Password!')
                return redirect('login')
        return render(request,'login.html')
    except:
        return redirect('login')
def register(request):
    try:
        if request.method == 'POST':
            name=request.POST['name']
            rollno=request.POST['roll']
            dob=request.POST['dob']
            email=request.POST['email']
            pass1=request.POST['password']
            pass2=request.POST['confirmpassword']

            if(pass1!=pass2):
                messages.info(request,'Password does not match!')
                return redirect('register')
            if (User.objects.filter(username=rollno).exists()):
                messages.info(request,'Roll No. already exists!')
                return redirect('register')
            if (User.objects.filter(email=email).exists()):
                messages.info(request,'Email already exists!')
                return redirect('register')
            else:     
                user=User.objects.create_user(username=rollno,first_name=name,last_name=dob,email=email,password=pass1)
                user.save()
                return redirect('login')

        else:
            return render(request,'register.html')
    except:
        return redirect('register')
    
def logout(request):
    auth.logout(request)
    return redirect('/')