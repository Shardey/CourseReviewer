from __future__ import division # Python 2.7 divides integers as integer so this is needed (Aalto default python is 2.7) --tr
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from ratings.models import Course, Review
from ratings.forms import SearchForm, ReviewForm
from django.db.models import Q

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
            course_list = Course.objects.all()
            
    

    ####
    # From Course: id,name,code,year,lecturer,myCourses_link
    # From Review: overall, lectures, assignments, workload into ratings[]
    # End result: id,name,code,year,lecturer,myCourses_link,overall,lectures,assignments,
    # workload,comments[], amount_of_reviews,my_review
    # Where my_comment contains the review of the current user if any
    
    # Because the end result of this system is that there are a lot more reviews
    # than there are courses, the algorithm that runs through the reviews once
    # runs faster than the one that runs through courses once.
    # Running it this way makes the calculating the averages easier however.

    course_list_final = [] # Init final list of course data along with reviews
    
    for course in course_list:

        #initialize the base data and the review counter
        course_data=[course.id,course.name,course.course_code,course.year,course.lecturer,
                     course.myCourses_link,0,0,0,0,[],0,[]]
        count = 0
        my_review = [0,0,0,0,[]]
        
        review_list = Review.objects.filter(course_id__exact=course.id)
        for review in review_list:
            if course.id == review.course_id_id:
                course_data[6] += review.overall
                course_data[7] += review.lectures
                course_data[8] += review.assignments
                course_data[9] += review.workload
                count += 1
                if request.user == review.user:
                    my_review[0] = review.overall
                    my_review[1] = review.lectures
                    my_review[2] = review.assignments
                    my_review[3] = review.workload

                    # Comments added only once, either into the general list or the user's list
                    if review.comments:
                        my_review[4].append(review.comments)
                elif review.comments:
                    course_data[10] = review.comments


        if count != 0:         # And remember to calculate the average of the review stars here
            course_data[6] /= count
            course_data[7] /= count
            course_data[8] /= count
            course_data[9] /= count
            
        course_data[11] = count
        course_data[12].append(my_review)

        # Add the compiled course data into the final array we want to pass to the template
        course_list_final.append(course_data)
        
    # Seems like the data is passed as integers. This is fine for now, likely need floats later. --tr
    return render(request,'ratings/index.html',{'course_list_final': course_list_final,
                                                'searchstring': searchstring,
                                                'add_review_form': ReviewForm()})



####
# This view adds a new review or updates the old review if the user already had
# reviewed this course. One review per user/course combination.
# Requires the user to be logged in.
@login_required
def add_review(request):
    if (request.method=='POST'):
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Find the review if it already exists for this user and course
            old_review = Reviews.objects.filter(user__exact=form.cleaned_data['user'],
                                                course_id__exact=form.cleaned_data['course_id'])

            if (not old_review):
            
                new_review = Review(course_id = form.cleaned_data['course_id'],
                                    user = form.cleaned_data['user'],
                                    overall = form.cleaned_data['overall'],
                                    lectures = form.cleaned_data['lectures'],
                                    assignments = form.cleaned_data['assignments'],
                                    workload = form.cleaned_data['workload'],
                                    comments = form.cleaned_data['comments'])
                new_review.save()
            else: # There was a review already, update its values
                old_review.course_id = form.cleaned_data['course_id']
                old_review.user = form.cleaned_data['user']
                old_review.overall = form.cleaned_data['overall']
                old_review.lectures = form.cleaned_data['lectures']
                old_review.assignments = form.cleaned_data['assignments']
                old_review.workload = form.cleaned_data['workload']
                old_review.comments = form.cleaned_data['comments']
                old_review.save()
        else:
            # error in submitting the form
            pass
    else:
        form = ReviewForm()
    return render(request,'ratings/index.html',{'searchstring': form.cleaned_data['searchstring'],
                                                'form': form})



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
