from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User # This might be good? -tr

class Course(models.Model):
    name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=200)
    year = models.DateField()
    lecturer = models.CharField(max_length=200)
    myCourses_link = models.URLField()

    def __unicode__(self):
        return unicode(self.name) or u''
    
class Review(models.Model):
    course_id = models.ForeignKey(Course)
    user = models.ForeignKey(User)             # !!!!!!!!Check this!!!!!!!
    overall = models.IntegerField('Overall stars')
    lectures = models.IntegerField('Lecture stars')
    assignments = models.IntegerField('Assignment stars')
    workload = models.IntegerField('Workload stars')
    comments = models.TextField(blank=True)

    def __unicode__(self): #What should this return really? Reviews dont have names..
        return unicode(self.course_id) or u''

