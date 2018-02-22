from __future__ import unicode_literals 
 
from django.shortcuts import render, HttpResponse, redirect 
from django.utils.html import escape
from django.contrib import messages
from .models import User
 
def login(request):
    if 'user_session' in request.session and request.session['user_session']:
        return redirect('/books/')
    else:
        return render(request, "users_app/index.html") 

def register(request):
    if 'user_session' in request.session and request.session['user_session']:
        return redirect('/books/')
    else:
        return render(request, "users_app/register.html")

def verify_login(request):
    response = User.objects.login_validator(request.POST)
    goto = '/books/'

    if response['status']:
        request.session['user_session']=response['user'].id

        clearSessions(request.session)
    else:
        request.session['email'] = request.POST['email']
        
        for tag, error in response['errors'].iteritems():
            messages.error(request, error, extra_tags=tag)

        goto = '/'

    return redirect(goto)

def create(request): 
    response = User.objects.registration_validator(request.POST)
    goto = '/books/'

    if response['status']:
        request.session['user_session']=response['user'].id

        clearSessions(request.session)
    else:
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']      
        
        for tag, error in response['errors'].iteritems():
            messages.error(request, error, extra_tags=tag)

        goto = '/register/'

    return redirect(goto)

def logout(request):
    del request.session['user_session']

    return redirect('/')

def clearSessions(session):
    if 'first_name' in session:
        del session['first_name']
    if 'last_name' in session:
        del session['last_name']
    if 'email' in session:
        del session['email']