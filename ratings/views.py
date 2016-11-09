from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from ratings.models import Course, Review

def index(request):
    course_list = Course.objects.all()
    review_list = Review.objects.all()

#### tästä jatketaan koska elämä on kivaa. seuraavaksi datatyyppi joka annetaan templatelle
    for course in course_list:
        comment_list = []
    if review_list:
        count = 0
        sum = 0
        for review in review_list:
            if review.course_id == course.id:
                count = count + review.overall
                sum = sum + 1
                comment_list.append(review.comments)


        count / sum
        comment_list
    else '0'
    endif







    return render_to_response('ratings/index.html',{'course_list': Course.objects.all(),
                                                    'review_list': Review.objects.all()})





def results(request, course_code):
    response = "You have searched for the course %s"
    return HttpResponse(response % course_code)

def loggedin(request):
    return render_to_response('ratings/loggedin.html',
                              {'username': request.user.username})

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