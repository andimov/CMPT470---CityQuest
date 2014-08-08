from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from cityquest.admin import newUserCreateForm

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/cq/cityquest/home')

def register_user(request):
    if request.method == 'POST':
        form = newUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cq/register_success/')

    args = {}
    args.update(csrf(request))
        
    args['form'] = newUserCreateForm()
    return render_to_response('register.html', args)

def register_success(request):
    return render_to_response('register_success.html')
