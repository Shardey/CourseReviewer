from __future__ import division # Python 2.7 divides integers as integer so this is needed (Aalto default python is 2.7) --tr
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from ratings.models import Course, Review
from ratings.forms import SearchForm
from django.db.models import Q

def index(request):
    ####
    # Make a list of courses based on search results and stuff it into course_list.
    
    course_list = Course.objects.all()
    user_review_list = []
    searchstring = []
    
    if (request.method == 'POST'): # We searched for a course
        form = SearchForm(request.POST)
        if form.is_valid():
            # Check for SQL injection in the search string here? --tr
            
            searchstring = form.cleaned_data['searchstring']
            course_list = Course.objects.filter(Q(name__contains=searchstring) | Q(course_code__contains=searchstring) | Q(lecturer__contains=searchstring))
            if (request.user):
                user_review_list = Review.objects.filter(user__exact=request.user)
        else:
            course_list = []

    

    ####
    # From Course: id,name,code,year,lecturer,myCourses_link
    # From Review: overall, lectures, assignments, workload into ratings[]
    # End result: name,code,year,lecturer,myCourses_link,overall,lectures,assignments,workload,comments[], amount_of_reviews
    
    # Because the end result of this system is that there are a lot more reviews
    # than there are courses, the algorithm that runs through the reviews once
    # runs faster than the one that runs through courses once.
    # Running it this way makes the calculating the averages easier however.

    course_list_final = [] # Init final list of course data along with reviews
    
    for course in course_list:
        #initialize the base data and the review counter
        course_data=[course.name,course.course_code,course.year,course.lecturer,course.myCourses_link,0,0,0,0,[],0]
        count = 0
        
        review_list = Review.objects.filter(course_id__exact=course.id)
        for review in review_list:
            if course.id == review.course_id_id:
                course_data[5] += review.overall
                course_data[6] += review.lectures
                course_data[7] += review.assignments
                course_data[8] += review.workload
                count += 1
                if review.comments: # Don't add empty comments to the list
                    course_data[9].append(review.comments)

        if count != 0:         # And remember to calculate the average of the review stars here
            course_data[5] /= count
            course_data[6] /= count
            course_data[7] /= count
            course_data[8] /= count
            
        course_data[10] = count
        # Add the compiled course data into the final array we want to pass to the template
        course_list_final.append(course_data)
        
    # Seems like the data is passed as integers. This is fine for now, likely need floats later. --tr
    return render(request,'ratings/index.html',{'course_list_final': course_list_final,
                                                'user_review_list': user_review_list,
                                                'searchstring': searchstring})



####
# This view adds a new review or updates the old review if the user already had
# reviewed this course. One review per user/course combination.
# Requires the user to be logged in.
@login_required
def add_review(request):
    if (request.method=='POST'):
        form = ReviewForm(request.POST)
    
    return render(request,'ratings/index.html')



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
