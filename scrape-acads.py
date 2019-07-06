#!/usr/bin/env python3
from django_extensions.management.jobs import DailyJob
import os
import standalone

standalone.run("lifeiitkbackend.settings")
from acads.models import AcadsModel
from events.models import EventModel
from tags.models import TagModel
from bs4 import BeautifulSoup
import re
import requests
import psycopg2
import numpy as np
from pandas import read_csv
import time
import tabula
from django.utils.dateparse import parse_date, parse_time
import json

semester = input("Enter semester (1 or 2) : ")
tabula.convert_into(
    "Course_Sem1.pdf", "output1.csv", output_format="csv", pages="all", guess=False
)
tabula.convert_into(
    "Course_Sem2.pdf", "output2.csv", output_format="csv", pages="all", guess=False
)


s = requests.Session()


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
print(name)

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


# In this list , index + 1 is the room no. (ex- L13 ) and the value at that index is the code associated to it in the url
room_ids = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 60, 61, 62]


r = s.post(
    "http://web.iitk.ac.in/lhcbooking/LHC/month.php?room=5&day=27&month=6&year=2019&area=5"
)
soup = BeautifulSoup(r.text, "html.parser")


class Job(DailyJob):
    def execute(self, soup):
        pk = 0
        for x in room_ids:
            r = s.post("http://web.iitk.ac.in/lhcbooking/LHC/month.php?room=" + str(x))
            soup = BeautifulSoup(r.text, "html.parser")
            for link in soup.find_all("div", {"class": "I"}):
                anchor = link.findChildren("a")
                href = anchor[0]["href"]
                title = anchor[0]["title"]

                start_time = title[:7]
                end_time = title[8:15]
                course_id = title[16:]
                course_id = course_id.upper()

                pattern = re.compile(r"day=\d{1,2}")
                match = pattern.search(href).group(0)
                day_no = match[4:]

                pattern = re.compile(r"month=\d{1,2}")
                match = pattern.search(href).group(0)
                month = match[6:]

                pattern = re.compile(r"year=\d{4}")
                match = pattern.search(href).group(0)
                year = match[5:]

                date = parse_date(year + "-" + month + "-" + day_no)
                # date = year + "-" + month + "-" + day_no
                start_time = parse_time(start_time)
                end_time = parse_time(end_time)

                if ids.count(course_id) != 0:
                    index = ids.index(course_id)
                    course_name = name[index]
                    venue = "L" + str(room_ids.index(x) + 1)
                    venue_id = room_ids.index(x)
                    booln = "True"
                    pk = pk + 1
                    integer = str(pk)
                    hash_tags = ["#" + course_id]
                    eventlist = EventModel.objects.all().order_by("event_id")
                    if len(eventlist) == 0:
                        event_id = 0
                    else:
                        event_id = eventlist.reverse()[0].event_id
                    tag_query = TagModel.objects.filter(name="acads")
                    if len(tag_query) == 0:
                        tid = TagModel.objects.order_by("tag_id").last().tag_id+1
                        tag = TagModel(tag_id=tid,name="acads")
                        tag.save()
                    else:
                        tag = tag_query[0]
                    data = EventModel(
                        event_id=event_id + 1,
                        title=course_name,
                        date=date,
                        start_time=start_time,
                        end_time=end_time,
                        day_long=False,
                        venue=venue,
                        venue_id=venue_id,
                        acad_state=True,
                        hash_tags=hash_tags,
                    )
                    data.tags.add(tag)
                    data.save()
                    corresponding_acads = AcadsModel.objects.filter(code=course_id)[0]
                    corresponding_acads.events.add(data)
                    corresponding_acads.save()


x = Job()
x.execute(soup)
