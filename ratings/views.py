from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf

def index(request):
    return render_to_response('ratings/index.html')

def results(request, course_code):
    response = "You have searched for the course %s"
    return HttpResponse(response % course_code)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ratings/register/complete')

    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('ratings/registration_form.html', token)

def registration_complete(request):
    return render_to_response('ratings/registration_complete.html')