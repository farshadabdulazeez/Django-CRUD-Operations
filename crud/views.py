
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#create functions here!
def signup_page(request):

    if 'user' in request.session:
        return redirect('home_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password= request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2 :
            return HttpResponse("Password is not matching!")

        user = User.objects.create_user(username,email,password)
        user.save()
        return redirect('login_page')
        

    return render(request,'signup_page.html')


@cache_control(no_cache=True, no_store=True)
def login_page(request):

    if 'user' in request.session:
        return redirect('home_page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:           
            request.session['user'] = username
            login(request,user)
            return redirect('home_page')
        else:            
            messages.error(request,'Incorrect username or password')
            return redirect('login_page')
        
    return render(request,'login_page.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='login_page')
def home_page(request):
    return render(request,'home_page.html')


@login_required(login_url='login_page')
@cache_control(no_cache=True, no_store=True)
def logout_page(request):
    logout(request)
    request.session.flush()
    return redirect('login_page')

@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_login')
def custom_admin(request):
    if 'admin' in request.session:
        cus = Customer.objects.all()

        context = {
            'cus' : cus,
        }
        return render(request,'admin_side.html',context)
    return redirect('admin_login')

@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_login')
def add(request):

    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        cus = Customer(
            name = name,  #first name is (modules name) and the (second name is index.html-> add section -> input -> field's name
            username = username,
            email = email,
        )
        cus.save()
        return redirect('custom_admin')   #url index file name
    
    return render(request, 'admin_side.html')

@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_login')
def edit(request):
    cus = Customer.objects.all()

    context = {
        'cus' : cus,
    }
    return redirect(request, 'admin_side.html', context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True, no_store=True)
def update(request, id):

    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        cus = Customer(
            id = id,        #id for updation, if it is not there will be a new record will be created!
            name = name,
            username = username,
            email = email,

        )
        cus.save()
        return redirect('custom_admin')
        
    return redirect(request, 'admin_side.html')

@cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_login')
def delete(request, id):

    cus = Customer.objects.filter(id = id)     #if id is deleted, the selected record will be deleted!
    cus.delete()

    context = {
        'cus' : cus,
    }

    return redirect('custom_admin')       #we don't want to redirect here


@cache_control(no_cache=True, no_store=True)
def admin_login(request):

    if 'admin' in request.session:
        return redirect('custom_admin')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_superuser:           
                request.session['admin'] = username
                login(request,user)
                return redirect('custom_admin')
            else:            
                messages.error(request,'Incorrect username or password')
                return redirect('admin_login')
        else:
            messages.error(request, 'Invalid credentials!')
        
    return render(request, 'admin_login.html')


@login_required(login_url='admin_login')
@cache_control(no_cache=True, no_store=True)
def admin_logout(request):

    if 'admin' in request.session:
    
        logout(request)
        request.session.flush()
        return redirect('admin_login')
    
    else:
        return redirect('admin_login')
    

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url='admin_login')
def admin_search(request):
    if request.method == 'POST':
        search_name = request.POST.get('search_name')
        search_query = Customer.objects.filter(username__startswith=search_name)
        context = {
            'cus': search_query  # Use the correct context variable name here
        }
        return render(request, 'admin_side.html', context)

    return redirect('custom_admin')
