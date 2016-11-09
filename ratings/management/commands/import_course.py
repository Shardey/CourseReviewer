#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from ratings.models import Course
import csv, sqlite3

class Command(BaseCommand):


    def handle(self, *args, **options):

        print Course.objects.all()

        conn = sqlite3.connect("/Users/joonaslinkola/Desktop/WWW/CourseReviewer-master/db.sqlite3")
        cur = conn.cursor()
        #cur.execute("DROP TABLE Course")
        #cur.execute("CREATE TABLE Course (name, course_code, year, lecturer, myCourses_link);")

        with open("/Users/joonaslinkola/Desktop/WWW/CourseReviewer-master/data.csv", 'rb') as fin:
            dr = csv.reader(fin)
            to_database = [(unicode(i[1], "utf8"),unicode(i[0], "utf8"),unicode(i[8], "utf8"),unicode(i[31], "utf8"),unicode(i[68], "utf8")) for i in dr]
            print 'hello'

        cur.executemany("INSERT INTO ratings_course (name, course_code, year, lecturer, myCourses_link) VALUES (?, ?, ?, ?, ?);", to_database)
        conn.commit()
        conn.close()
