from __future__ import division # Python 2.7 divides integers as integer so this is needed (Aalto default python is 2.7) --tr
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from ratings.models import Course, Review
from ratings.forms import SearchForm, ReviewForm, UserCreateForm
from django.db.models import Q
from django.contrib.auth import views as auth_views
import pdb

def index(request):
    ####
    # Make a list of courses based on search results and stuff it into course_list.
    
    course_list = []
    searchstring = []
    
    if (request.method == 'POST'): # We searched for a course
        form = SearchForm(request.POST)
        if form.is_valid():
            
            searchstring = form.cleaned_data['searchstring']
            course_list = Course.objects.filter(Q(name__contains=searchstring) |
                                                Q(course_code__contains=searchstring) |
                                                Q(lecturer__contains=searchstring))
        else:
#            course_list = Course.objects.all()
            course_list = Course.objects.filter(name__contains="bayesian")
    

    ####
    # From Course: id,name,code,year,lecturer,myCourses_link
    # From Review: overall, lectures, assignments, workload into ratings[]
    # End result: id,name,code,year,lecturer,myCourses_link,overall,lectures,assignments,
    # workload,comments[], amount_of_reviews[] ,my_review
    # Where my_comment contains the review of the current user if any
    
    # Because the end result of this system is that there are a lot more reviews
    # than there are courses, the algorithm that runs through the reviews once
    # runs faster than the one that runs through courses once.
    # Running it this way makes the calculating the averages easier however.

    course_list_final = [] # Init final list of course data along with reviews
    
    for course in course_list:

        #initialize the base data and the review counter
        course_data=[course.id, course.name, course.course_code, course.year, course.lecturer,
                     course.myCourses_link,0,0,0,0,[],[],[]]
        count = [0,0,0,0]
        my_review = [99,99,99,99,[]]
        
        review_list = Review.objects.filter(course_id__exact=course.id)
        for review in review_list:
            if course.id == review.course_id_id:
                if review.overall != 99:
                    course_data[6] += review.overall
                    count[0] += 1

                if review.lectures != 99:
                    course_data[7] += review.lectures
                    count[1] += 1

                if review.assignments != 99:
                    course_data[8] += review.assignments
                    count[2] += 1

                if review.workload != 99:
                    course_data[9] += review.workload
                    count[3] += 1
                
                if request.user == review.user:
                    my_review[0] = review.overall
                    my_review[1] = review.lectures
                    my_review[2] = review.assignments
                    my_review[3] = review.workload

                    # Comments added only once, either into the general list or the user's list
                    if review.comments:
                        my_review[4].append(review.comments)
                elif review.comments:
                    course_data[10].append(review.comments)

# And remember to calculate the average of the review stars here
        if count[0] != 0:         
            course_data[6] /= count[0]
        if count[1] != 0:
            course_data[7] /= count[1]
        if count[2] != 0:
            course_data[8] /= count[2]
        if count[3] != 0:
            course_data[9] /= count[3]
            
        course_data[11].append(count)
        course_data[12].append(my_review)

        # Add the compiled course data into the final array we want to pass to the template
        course_list_final.append(course_data)
        
    # Seems like the data is passed as integers. This is fine for now, likely need floats later. --tr
    return render(request,'ratings/index.html',{'course_list_final': course_list_final,
                                                'searchstring': searchstring,
                                                'add_review_form': ReviewForm()})



####
# This view adds a new review or updates the old review if the user already had
# reviewed this course. A user can review each course only once but may later
# change the review.
# Requires the user to be logged in.

@login_required
def add_review(request):
    if (request.method=='POST'):
        form = ReviewForm(request.POST)
        if form.is_valid():
            searchstring = "bayes"
            # Find the review if it already exists for this user and course
            old_review = Review.objects.filter(user__exact=form.cleaned_data['user'],
                                                course_id__exact=form.cleaned_data['course_id']).first()

            if (old_review):
                f = ReviewForm(request.POST, instance=old_review)
                pdb.set_trace
                f.save()
                
            else:
                f = ReviewForm(request.POST)
                f.save()

        else:
            pass
            #            searchstring = "math"
            # error in receiving form from template
    else:
        pass
    return render(request,'ratings/index.html',{'searchstring': searchstring})
#    return redirect('/ratings/index.html',{'searchstring': searchstring})



def loggedin(request):
    if 'login' in request.POST:
        return render_to_response('ratings/loggedin.html',
                                  {'username': request.user.username})

def logout(request):
    auth_views.logout(request)
    return render(request, 'ratings/index.html')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ratings/register/complete')

    else:
        form = UserCreateForm()
        token = {}
        token.update(csrf(request))
        token['form'] = form

        return render_to_response('ratings/registration_form.html', token)

def registration_complete(request):
    return render_to_response('ratings/registration_complete.html')
