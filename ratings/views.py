from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from ratings.models import Course, Review
from django.template.loader import get_template 
from django.template import Context
from operator import attrgetter

def search(request):

    query = request.GET['q']

    t = get_template('ratings/index.html')
    c = Context({'query': query,})

    course_list_filtered_name = Course.objects.filter(name__icontains = query)
    course_list_filtered_code = Course.objects.exclude(name__icontains = query).filter(course_code__icontains = query)
    course_list_filtered_lecturer = Course.objects.exclude(name__icontains = query).exclude(course_code__icontains = query).filter(lecturer__icontains = query)

    course_list_filtered = course_list_filtered_name | course_list_filtered_code | course_list_filtered_lecturer
    
    review_list = Review.objects.all()
    
    course_list_final = [] # Init final list of course data along with reviews
    
    for course in course_list_filtered:
        #initialize the base data and the review counter
        course_data=[course.name,course.course_code,course.year,course.lecturer,course.myCourses_link,0,0,0,0,[]]
        count = 0

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
            
        # Add the compiled course data into the final array we want to pass to the template
        course_list_final.append(course_data)
        
    # Seems like the data is passed as an integer. This is fine for now. --tr
    # return render(request,'ratings/index.html',{'course_list_final': course_list_final})
    return render(request,'ratings/index.html',{'course_list_final': course_list_final, 'query': query})

def index(request):
    ####
    # Make a list of courses based on search results and stuff it into course_list. Review list
    # remains the list of all reviews. The averages will be calculated further below. --tr
    
    course_list = Course.objects.all()
    review_list = Review.objects.all()

    ####
    # From Course: id,name,code,year,lecturer,myCourses_link
    # From Review: overall, lectures, assignments, workload into ratings[]
    # End result: name,code,year,lecturer,myCourses_link,overall,lectures,assignments,workload,comments[]
    
    # Because the end result of this system is that there are a lot more reviews
    # than there are courses, the algorithm that runs through the reviews once
    # runs faster than the one that runs through courses once.
    # Running it this way makes the calculating the averages easier to read however.

    course_list_final = [] # Init final list of course data along with reviews
    
    for course in course_list:
        #initialize the base data and the review counter
        course_data=[course.name,course.course_code,course.year,course.lecturer,course.myCourses_link,0,0,0,0,[]]
        count = 0

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
            
        # Add the compiled course data into the final array we want to pass to the template
        course_list_final.append(course_data)
        
    # Seems like the data is passed as an integer. This is fine for now. --tr
    return render(request,'ratings/index.html',{'course_list_final': course_list_final})


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
