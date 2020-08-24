## Events Api

### Create

Creating an event(error in owned_tags initialiation SOLVED)
after that we can create an event

```
Endpoint : /api/events/create/
Method : POST
Authentication Required

Request Body:
{
    "title":"a1",
    "description":"p",
    "date":"2020-08-09",
    "start_time":"08:30:00",
    "end_time":"09:30:00",
    "day_long":"False",
    "summary":"asfafaf",
    "venue":"C",
    "venue_id":1,
    "tag_name":"Pclub",
    "hash_tags":["#pclub"]
}

Response: None
Response Code Meanings:
200 - ok
```

### Event in Month

events in particular month(error in rendering after solving it)

```
Endpoint : /api/events/view/month/

Method : GET

Request Body:
Query_set:
?month=08&year=2020

Response:
[
    {
        "event_id": 1,
        "title": "a",
        "description": "performance1",
        "date": "2020-08-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "CCD",
        "venue_id": 1,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    },
    {
        "event_id": 2,
        "title": "a1",
        "description": "p",
        "date": "2020-08-09",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "C",
        "venue_id": 1,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    }
]
Response Code Meanings:
200 - ok
```

### Venue

events in particular Venue(error in rendering after solving it)

```
Endpoint : /api/events/view/venue/

Method : GET


Request Body:
Query_set:
?venue=2

Response:
[
    {
        "event_id": 2,
        "title": "a1",
        "description": "p",
        "date": "2020-08-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "C",
        "venue_id": 2,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    }
]
Response Code Meanings:
200 - ok
```

### Event Feed

```
Endpoint :/api/events/feed/

Method : GET

Authentication Required

Response:
[
    {
        "event_id": 1,
        "title": "a",
        "description": "performance1",
        "date": "2020-08-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "CCD",
        "venue_id": 1,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    },
    {
        "event_id": 2,
        "title": "a1",
        "description": "p",
        "date": "2020-08-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "C",
        "venue_id": 2,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    }
]

Response Code Meanings:
200 - ok
```

### Event feed month wise

```
Endpoint : /api/events/feed/month/

Method : GET

Authentication Required

Request Body:
Query_set:
?month=08&year=2020

Response:
[
    {
        "event_id": 2,
        "title": "a1",
        "description": "p",
        "date": "2020-08-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "C",
        "venue_id": 2,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    }
]
Response Code Meanings:
200 - ok
```

### Event field Tag wise

(error now not defined after solving it)

```
Endpoint : /api/events/view/tagged_events/

Method : GET

Request Body:
Query_set:
?tag_name=Pclub

Response:
[
    {
        "event_id": 1,
        "title": "a",
        "description": "performance1",
        "date": "2020-09-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "CCD",
        "venue_id": 1,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    },
    {
        "event_id": 2,
        "title": "a1",
        "description": "p",
        "date": "2020-08-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "C",
        "venue_id": 2,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    }
]
Response Code Meanings:
200 - ok
```

### events related to acads

```
Endpoint : /api/events/acads/

Method : GET

Request Body:
Query_set:
?month=08&year=2020

Response:
[
    {
        "event_id": 2,
        "title": "a1",
        "description": "p",
        "date": "2020-08-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "C",
        "venue_id": 2,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    }
]
Response Code Meanings:
200 - ok
```

### All events monthwise

```
Endpoint : /api/events/all/

Method : GET

Request Body:
Query_set:
?month=09&year=2020

Response:
[
    {
        "event_id": 1,
        "title": "a",
        "description": "performance1",
        "date": "2020-09-08",
        "start_time": "08:30:00",
        "end_time": "09:30:00",
        "venue": "CCD",
        "venue_id": 1,
        "tags": [
            {
                "tag_id": 1,
                "name": "Pclub",
                "description": ""
            }
        ],
        "acads": [
            {
                "course_id": 1,
                "name": "ESC",
                "code": "101A"
            }
        ],
        "day_long": false,
        "summary": "asfafaf",
        "acad_state": false,
        "hash_tags": [
            "#pclub"
        ]
    }
]
Response Code Meanings:
200 - ok
```

### Deleting a event

```
Endpoint : /api/events/delete/

Method : DELETE

Request Body:
{
"event_id" : 2
}

Response:
None
Response Code Meanings:
200 - ok
```

## User

### Register

Validate email address by sending mail and allow user to set their password

```
Endpoint : /api/users/register/

Method : POST

Request Body:
{
"roll" : 190512
}

Response:
None
Response Code Meanings:
202 - Accepted (if you are entered for first time)
403- forbidden (if you have already registered)
400 - BAD Request

```

### Set password for first time

Allow user to set thier password for the very first time

```
Endpoint : /api/users/verify/code=<str:token>/

Method : POST

Request Body:
{
"password" : "123"
}

Response:
{
    "status": "success",
    "code": 200,
    "message": "Password set succesfully and now you are registered"
}
Response Code Meanings:
200 - OK (if password set successfully)
401- UNAUTHORIZED (token already used)
400 - Invalid Request

```

### Reset password email

Send email to reset your password

```
Endpoint : /api/users/resetpassemail/

Method : POST

Request Body:
{
"roll" : 190512
}

Response:
None
Response Code Meanings:
206- Please set up email host details!
400 - invalid request!
```

### Change password

Allow to change password

```
Endpoint : /api/users/resetpass/code=<str:token>/

Method : POST

Request Body:
{
"new_password1" : "1234",
"new_password2" : "1234",
"old_password" : "123"
}

Response:
{
    "status": "success",
    "code": 200,
    "message": "Password reset succesfull and now you can login"
}
Response Code Meanings:
200 - OK (if password set successfully)
401- UNAUTHORIZED (if wrong password given)
400 - Invalid Request

```
