from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.
def login(request):
    if request.is_ajax() and request.method == 'POST':
        #Get form values
        #username = request.POST['username']
        request.POST.get("csrfmiddlewaretoken")
        username = request.POST.get("username", "")
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request,user)
            data = {
                'status' : 1
            }
            return JsonResponse(data)
            #return redirect('dashboard')
        else:
            data = {
                'status' : 2
            }
            return JsonResponse(data)
    else:
        return render(request, 'account/login.html')

def dashboard(request):
    users = User.objects.all()
    user = request.user
    context = {
        'users': users,
        'user' : user
        }              
    return render(request, 'account/dashboard.html', context)

def register(request):
    if request.is_ajax and request.method == 'POST':
        #Get form values
        request.POST.get("csrfmiddlewaretoken")
        first_name = request.POST.get("first_name","")
        last_name = request.POST.get("last_name","")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_superuser = (request.POST.get("is_superuser", "0") == "1")
        #is_superuser = False
        #if (request.POST.get("is_superuser", "0") == "1"):
            #is_superuser = True
        is_staff = (request.POST.get("is_staff","0") == "1")
        #print(is_staff)

#check if password matches        
        if User.objects.filter(username__iexact = username ).exists():
            data = {
                'status': 1
                #alert user exists
            }
            return JsonResponse(data)
            #return redirect('register')
        else:
            #check if email matches
            if User.objects.filter( email__iexact = email ).exists():
                data = {
                    'status': 2
                    #alert email exists
                }
                return JsonResponse(data)
                #return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password = password, first_name =first_name, last_name = last_name, is_superuser = is_superuser, is_staff = is_staff)
                user.save()
                data = {
                'status': 3 
                #alert user is saved
                }  
                return JsonResponse(data)
                #return redirect('login')
    else: 
        users = User.objects.all()
        context = {
            'users': users
        }              
        return render(request, 'account/dashboard.html', context)

def viewuser(request, user_id):
    try:
        #user_details = get_object_or_404(User, pk = user_id)
        user_details = User.objects.get(pk=user_id)
        context = {
                'user_details': user_details
            }
        return render(request, 'account/viewuser.html', context)
    except:
        return render(request, 'account/404.html')

def edituser(request, user_id):
    try:
        #user_details = get_object_or_404(User, pk = user_id)
        user_details = User.objects.get(pk=user_id)
        context = {
                'user_details': user_details
            }
        return render(request, 'account/edituser.html', context)
    except:
        return render(request, 'account/404.html')

def updateuser(request, user_id):
    if request.is_ajax and request.method == 'POST':
        #Get form values
        request.POST.get("csrfmiddlewaretoken")
        first_name = request.POST.get("first_name","")
        last_name = request.POST.get("last_name","")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_superuser = (request.POST.get("is_superuser", "0") == "1")
        #is_superuser = False
        #if (request.POST.get("is_superuser", "0") == "1"):
            #is_superuser = True
        is_staff = (request.POST.get("is_staff","0") == "1")
        #print(is_staff)

        #check if username matches 
        
        
        if User.objects.filter(username__iexact = username ).exclude( pk = user_id ).exists():
            data = {
                'status': 1
                #alert user exists
            }
            return JsonResponse(data)
            #return redirect('register')
        #check if email matches
        if User.objects.filter( email = email ).exclude( pk=user_id ).exists():
            data = {
                'status': 2
                #alert email exists
            }
            return JsonResponse(data)
        if len(password)!=0 and len(password)<6:
            pass
        user = User.objects.get(pk=user_id)
        user.username = username
        user.email = email
        if len(password)!=0:
            user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.save()
        data = {
        'status': 3 
        #alert user is saved
        }  
        return JsonResponse(data)
    try: 
        user_details = User.objects.get( pk = user_id )
        context = {
            'user_details': user_details
        }              
        return render(request, 'account/edituser.html', context)
    except:
        return render(request, 'account/404.html')


def deleteuser(request, user_id):
    if request.is_ajax and request.method == 'POST':
        try:
            #user_details = get_object_or_404(User, pk = user_id)
            user_details = User.objects.get(pk=user_id)
            user_details.delete()
            data = {
                'status':1
            }
            return JsonResponse(data)
        except:
            return render(request, 'account/404.html')
    else:
        users = User.objects.all()
        context = {
            'users': users
        }              
        return render(request, 'account/dashboard.html', context)  


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')