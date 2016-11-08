from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, you are at ratings index.")

def results(request, course_code):
    response = "You have searched for the course %s"
    return HttpResponse(response % course_code)



