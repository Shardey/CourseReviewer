from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User # This might be good? -tr

class Course(models.Model):
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    year = models.IntegerField()
    lecturer = models.CharField(max_length=200)
    myCourses_link = models.URLField()

    def get_name(self):
        return self.name

    def get_course_code(self):
        return self.course_code

    def get_year(self):
        return self.year

    def get_lecturer(self):
        return self.lecturer

    def get_myCourses_link(self):
        return self.myCourses_link

    def __str__(self):
        return self.name
    
class Review(models.Model):
    course_code = models.ForeignKey(Course)
    user = models.ForeignKey(User)             # !!!!!!!!Check this!!!!!!!
    overall = models.IntegerField('Overall stars')
    lectures = models.IntegerField('Lecture stars')
    assignments = models.IntegerField('Assignment stars')
    workload = models.IntegerField('Workload stars')
    comments = models.TextField()

    def get_course_code(self):
        return self.course_code

    def get_user(self):
        return self.user
    
    def get_overall(self):
        return self.overall

    def get_lectures(self):
        return self.lectures

    def get_assignments(self):
        return self.assignments

    def get_workload(self):
        return self.workload

    def comments(self):
        return self.comments

    
    def __str__(self): #What should this return really? Reviews dont have names..
        return self.comments 
