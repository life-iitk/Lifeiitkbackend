#!/usr/bin/env python3
from django_extensions.management.jobs import DailyJob

from bs4 import BeautifulSoup
import re
import requests
import psycopg2
import numpy as np
from pandas import read_csv
import time
import tabula
from django.utils.dateparse import parse_date, parse_time

semester = input("Enter semester (1 or 2) : ")
tabula.convert_into(
    "Course_Sem1.pdf", "output1.csv", output_format="csv", pages="all", guess=False
)
tabula.convert_into(
    "Course_Sem2.pdf", "output2.csv", output_format="csv", pages="all", guess=False
)

conn = psycopg2.connect(
    host="localhost", database="students", user="aditya", password="password"
)
c = conn.cursor()
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
pkacad = 0

for course_ids in ids:
    index = ids.index(course_ids)
    acad_name = name[index][:30]
    pkacad = pkacad + 1
    pkacads = str(pkacad)
    c.execute(
        "INSERT INTO acads_acadsmodel (course_id,name,code) VALUES (%s,%s,%s) ON CONFLICT(course_id) DO UPDATE SET name=Excluded.name, code=Excluded.code",
        (pkacads, acad_name, course_ids),
    )


# In this list , index + 1 is the room no. (ex- L13 ) and the value at that index is the code associated to it in the url
room_ids = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 60, 61, 62]


r = s.post(
    "http://web.iitk.ac.in/lhcbooking/LHC/month.php?room=5&day=27&month=6&year=2019&area=5"
)
soup = BeautifulSoup(r.text, "html.parser")


class Job(DailyJob):
    def execute(self, soup, c):
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

                date = parse_date(year + "-" + month + "-" + day_no).strftime(
                    "%Y-%m-%d"
                )
                # date = year + "-" + month + "-" + day_no
                start_time = parse_time(start_time).strftime("%H:%M")
                end_time = parse_time(end_time).strftime("%H:%M")

                if ids.count(course_id) != 0:
                    index = ids.index(course_id)
                    course_name = name[index]
                    venue = "L" + str(room_ids.index(x))
                    venue_id = str(room_ids.index(x))
                    booln = "True"
                    pk = pk + 1
                    integer = str(pk)
                    day_long = "False"
                    sql = "INSERT INTO events_eventmodel (event_id,title,date,start_time,end_time,day_long,venue,venue_id,acad_state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(event_id) DO UPDATE SET title=Excluded.title, date=Excluded.date, start_time=Excluded.start_time, end_time=Excluded.end_time, day_long=Excluded.day_long, venue=Excluded.venue, venue_id=Excluded.venue_id, acad_state=Excluded.acad_state"
                    c.execute(
                        sql,
                        (
                            integer,
                            course_name,
                            date,
                            start_time,
                            end_time,
                            day_long,
                            venue,
                            venue_id,
                            booln,
                        ),
                    )
                    conn.commit()
        conn.close()


x = Job()
x.execute(soup, c)
