#!/usr/bin/env python3
from django_extensions.management.jobs import DailyJob
import os
import standalone

standalone.run("lifeiitkbackend.settings")
from acads.models import AcadsModel
from events.models import EventModel
from tags.models import TagModel
import re
import psycopg2
import numpy as np
from pandas import read_csv
import time
import tabula
import json
import datetime
from background_task import background
from users.tasks import execute
from background_task.models import Task

semester = input("Enter semester (1 or 2) : ")
tabula.convert_into(
    "Course_Sem1.pdf", "output1.csv", output_format="csv", pages="all", guess=False
)
tabula.convert_into(
    "Course_Sem2.pdf", "output2.csv", output_format="csv", pages="all", guess=False
)



def getCourses(array):
    course_id = []
    course_name = []
    for x in range(len(array)):
        detail = array[x]
        if detail == "":
            break

        for y in range(13):
            # print(detail)
            if detail[-1 - y] == "(":
                course_id.append(detail[-y:])
                course_name.append(detail[: -y - 1])
                break
    course_id = [courses.replace(" ", "") for courses in course_id]
    course_id = [courses.replace(")", "") for courses in course_id]

    return course_name, course_id


def getArray(sem=1):
    depts = ["AE","BSBE","CHE","CHM","CE","CSE","ES","EE","ART","IME","ESO","MSE","MSO","MTH","PHY","DES","PSE","HSS"]
    csv = read_csv("output" + str(sem) + ".csv", usecols=[1, 2])
    array = np.asarray(csv)
    array = np.delete(array, 0)
    array = list(filter(lambda a: str(a) != "nan", array))
    array = list(filter(lambda a: a != "Branch", array))
    array = list(filter(lambda a: a != "Course Name/Group Name", array))
    array = np.delete(array, 0)
    array = list(filter(lambda a: str(a) != "nan", array))

    array2 = []

    length = len(array)
    array2.append(array[0])

    for i in range(1, length):
        if array[i] in depts:
            continue
        elif len(array[i]) >= 4 and (array[i][-3] == ")" and array[i][-2] == "/"):
            array2[-1] += " " + array[i][:-2]
            array2.append("")
        elif array[i][-1] == ")":
            array2[-1] += " " + array[i]
            array2.append("")
        else:
            array2[-1] += " " + array[i]

        array2 = [elem.strip() for elem in array2]
        array2 = [courses.replace("ME ", "") for courses in array2]
        array2 = [courses.replace("LT ", "") for courses in array2]
    return array2


array1 = getArray(semester)
name, ids = getCourses(array1)

for course_ids in ids:
    index = ids.index(course_ids)
    acad_name = name[index]
    acad_list = AcadsModel.objects.all().order_by("course_id")
    if len(acad_list) == 0:
        course_id = 0
    else:
        course_id = acad_list.reverse()[0].course_id + 1
    if len(AcadsModel.objects.filter(course_id=course_id)) == 0:
        data = AcadsModel(course_id=course_id, name=acad_name, code=course_ids)
        data.save()


execute(name,ids,repeat=Task.DAILY)
