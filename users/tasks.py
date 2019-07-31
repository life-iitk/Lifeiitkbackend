from background_task import background
from users.utils import send_push_message
from tags.models import TagModel
import datetime
import re
from django.utils.dateparse import parse_date, parse_time
import requests
from bs4 import BeautifulSoup
from acads.models import AcadsModel
from events.models import EventModel
from tags.models import TagModel

@background(schedule=5)
def notify_new_event(message,tag_name):
    tag = TagModel.objects.get(name=tag_name)
    # print("\nbefore loop\n")
    for user in tag.users.all():
        for token in user.tokens.all():
            # print("in admin task")
            send_push_message(token.token,message)

@background(schedule=5)
def execute(name,ids):
        # In this list , index + 1 is the room no. (ex- L13 ) and the value at that index is the code associated to it in the url
    room_ids = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 60, 61, 62]


    month = datetime.datetime.now().month
    if month != 12:
        list_months = [ month , 1  ]
    else:
        list_months = [ month , month + 1]

    s = requests.Session()
    r = s.post(
    "http://web.iitk.ac.in/lhcbooking/LHC/month.php?room=5&day=27&month=6&year=2019&area=5"
    )
    soup = BeautifulSoup(r.text, "html.parser")
    pk = 0
    for x in room_ids:
        for month in list_months:
            r = s.post("http://web.iitk.ac.in/lhcbooking/LHC/month.php?room=" + str(x)+"&month=" +str(month))
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
                        event_id = eventlist.reverse()[0].event_id + 1
                    data = EventModel(
                        event_id=event_id,
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
                    exists = False
                    check_event_list = EventModel.objects.filter(title=course_name,date=date,start_time=start_time,end_time=end_time,day_long=False,venue=venue,venue_id=venue_id,acad_state=True,hash_tags=hash_tags)
                    if check_event_list.exists() :
                        exists = True
                    
                    if not exists :
                        data.save()
                        tag_query = TagModel.objects.filter(name="acads")
                        if len(tag_query) == 0:
                            tid = TagModel.objects.order_by("tag_id").last().tag_id+1
                            tag = TagModel(tag_id=tid,name="acads")
                            tag.save()
                        else:
                            tag = tag_query[0]

                        data.tags.add(tag)

                        data.save()
                        corresponding_acads = AcadsModel.objects.filter(code=course_id)[0]
                        corresponding_acads.events.add(data)
                        corresponding_acads.save()
