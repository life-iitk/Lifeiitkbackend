#!/usr/bin/env python3
from django_extensions.management.jobs import DailyJob

from bs4 import BeautifulSoup
import re
import requests
import psycopg2

conn = psycopg2.connect(
    host="localhost", database="students", user="aditya", password="password"
)
c = conn.cursor()
s = requests.Session()
s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/Main_Frameset.jsp")
s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/Main_Intro.jsp?frm='SRCH'")
s.get("https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITK_Srch.jsp?typ=stud")

headers = {
    "Referer": "https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITK_Srch.jsp?typ=stud"
}

headers1 = {
    "Referer": "https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchStudRoll_new.jsp"
}

payload = {
    "k4": "oa",
    "numtxt": "",
    "recpos": 0,
    "str": "",
    "selstudrol": "",
    "selstuddep": "",
    "selstudnam": "",
    "txrollno": "",
    "Dept_Stud": "",
    "selnam1": "",
    "mail": "",
}

payload1 = {"typ": ["stud"] * 12, "numtxt": "", "sbm": ["Y"] * 12}
TOTAL = 8385
r = s.post(
    "https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchStudRoll_new.jsp",
    headers=headers,
    data=payload,
)
soup = BeautifulSoup(r.text, "html.parser")


class Job(DailyJob):
    def process_response_soup(self, soup, c):

        for link in soup.select(".TableText a"):
            roll = link.get_text().strip()
            payload1["numtxt"] = roll
            r1 = s.post(
                "https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchRes_new.jsp",
                headers=headers1,
                data=payload1,
            )
            soup1 = BeautifulSoup(r1.text, "html.parser")

            name = ""
            program = ""
            dept = ""
            hall = ""
            room = ""
            username = ""
            blood_group = ""
            gender = ""
            hometown = ""

            for para in soup1.select(".TableContent p"):
                body = para.get_text().strip()
                field = body.split(":")
                key = field[0].strip()
                value = field[1].strip()
                if key == "Name":
                    name = value.lower().title()
                elif key == "Program":
                    program = value
                elif key == "Department":
                    dept = value.lower().title()
                elif key == "Hostel Info":
                    if len(value.split(",")) > 1:
                        hall = value.split(",")[0].strip()
                        room = value.split(",")[1].strip()
                elif key == "E-Mail":
                    if len(value.split("@")) > 1:
                        username = value.split("@")[0].strip()
                elif key == "Blood Group":
                    blood_group = value
                elif key == "Gender":
                    if len(value.split("\t")) > 1:
                        gender = value.split("\t")[0].strip()
                else:
                    print("{} {}".format(key, value))

            body = soup1.prettify()
            if len(body.split("Permanent Address :")) > 1:
                address = body.split("Permanent Address :")[1].split(",")
                if len(address) > 2:
                    address = address[len(address) - 3 : len(address) - 1]
                    hometown = "{}, {}".format(address[0], address[1])
                    image = (
                        "http://oa.cc.iitk.ac.in/Oa/Jsp/Photo/" + str(roll) + "_0.jpg"
                    )
                    c.execute(
                        "INSERT INTO users_user (roll, username,image,name,program,dept,hall,room,blood_group,gender,hometown) VALUES ("
                        + roll.replace("'", "")
                        + ", '"
                        + username.replace("'", "")
                        + "','"
                        + image.replace("'", "")
                        + "', '"
                        + name.replace("'", "")
                        + "', '"
                        + program.replace("'", "")
                        + "', '"
                        + dept.replace("'", "")
                        + "', '"
                        + hall.replace("'", "")
                        + "', '"
                        + room.replace("'", "")
                        + "', '"
                        + blood_group.replace("'", "")
                        + "', '"
                        + gender.replace("'", "")
                        + "', '"
                        + hometown.replace("'", "")
                        + "') ON CONFLICT(roll) DO UPDATE SET name=Excluded.name, image=Excluded.image, username=Excluded.username, program=Excluded.program, dept=Excluded.dept, hall=Excluded.hall, blood_group=Excluded.blood_group,gender=Excluded.gender,hometown=Excluded.hometown,room=Excluded.room"
                    )
                    # c.execute("INSERT INTO users_user (user_img ) VALUES" ('http://oa.cc.iitk.ac.in/Oa/Jsp/Photo/' + str(roll) + '_0.jpg'))

    def execute(self, soup, c):
        for link in soup.select(".DivContent"):
            substituted = re.sub(r"\s+", " ", link.text)
            pattern = re.compile(
                r"\s*You are viewing 1 to 12 records out of (\d+) records\s*"
            )
            match = pattern.match(substituted)
            TOTAL = int(match.group(1))
            print("Total: {}".format(TOTAL))
        self.process_response_soup(soup, c)

        for i in range(12, TOTAL + 1, 12):
            payload["recpos"] = i
            r = s.post(
                "https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchStudRoll_new.jsp",
                headers=headers,
                data=payload,
            )
            soup = BeautifulSoup(r.text, "html.parser")
            self.process_response_soup(soup, c)

            print("Processed {}".format(i + 12))
            conn.commit()
        conn.close()


x = Job()
x.execute(soup, c)

