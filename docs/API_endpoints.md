# API Endpoints Documentation (R5)

---

## Table of Contents

[Auth Routes](#auth-routes)

[User Routes](#user-routes)

[Admin Routes](#admin-routes)

[Game Routes](#game-routes)

---

## Auth Routes

---

### /auth/register/

- Methods: POST

- Arguments: None

- Description: Register new user in the database

- Authentication: None

- Authorization: None

- Request Body:

```json
{
    "name": "John Smith",
    "email": "test@abc.com",
    "password": "abc"
}
```

- Response Body:

Successfully registered user (status code: 201):

```json
{
    "message": "You are now registered!",
    "user": {
        "id": 4,
        "name": "John Smith",
        "email": "test@abc.com",
        "date_joined": "2022-11-13",
        "is_admin": false,
        "games": [],
        "notes": []
    }
}
```

Email already in use (status code: 409):

```json
{
    "error": "Email address already in use"
}
```

No email or password provided (status code: 400)

```json
{
    "error": "The field 'email/password' is required."
}
```

### /auth/login/

- Methods: POST

- Arguments: none

- Description: Login the user

- Authentication: none

- Authorization: none

- Request Body:

```json
{
    "email": "test@abc.com",
    "password": "abc"
}
```

- Response Body:

Successfully logged in the user (status code: 200):

```json
{
    "message": "You have successfully logged in!",
    "email": "test@abc.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODMyNDg4MywianRpIjoiNTU1NzZhYmYtOWE0OS00ZjA5LWE4NDItMGU2ZDhmMTA2NzQwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE2NjgzMjQ4ODMsImV4cCI6MTY2ODQxMTI4M30._zK4sbrjHG9twm18v7Oi1qLSyZMVcDS6-QOgBQVhQEY",
    "is_admin": false
}
```

Incorrect email or password (status code: 401):

```json
{
    "error": "Invalid email or password - please try again."
}
```

---

## User Routes

---

/users/profile/

- Methods: GET

- Arguments: none

- Description: Read user profile

- Authentication: jwt_required

- Authorization: Bearer token

- Request Body: none

- Response Body:

```json
{
  "id": 3,
  "name": "James White",
  "email": "jameswhite@abc.com",
  "date_joined": "2021-05-23",
  "is_admin": false,
  "games": [
    {
      "title": "God of War Ragnarok",
      "status": "Playing"
    },
    {
      "title": "Bayonetta 3",
      "status": "Want to Play"
    }
  ],
  "notes": [
    {
      "id": 2,
      "description": "Up to second bossfight",
      "date": "2022-11-13",
      "tag": "Progress",
      "game": {
        "title": "God of War Ragnarok",
        "status": "Playing"
      }
    }
  ]
}
```

/users/profile/

- Methods: PUT or PATCH

- Arguments: none

- Description: Update user details

- Authentication: jwt_required

- Authorization: Bearer token only

- Request Body:

```json
{
    "name": "James Anthony White",
    "email": "jamesanthonywhite@gmail.com",
    "password": "password123"
}
```

- Response Body:

```json
{
    "message": "You have updated your details!",
    "user": {
        "id": 3,
        "name": "James Anthony White",
        "email": "jamesanthonywhite@gmail.com",
        "date_joined": "2021-05-23",
        "is_admin": false,
        "games": [
            {
                "title": "God of War Ragnarok",
                "status": "Playing"
            },
            {
                "title": "Bayonetta 3",
                "status": "Want to Play"
            }
        ],
        "notes": [
            {
                "id": 2,
                "description": "Up to second bossfight",
                "date": "2022-11-13",
                "tag": "Progress",
                "game": {
                    "title": "God of War Ragnarok",
                    "status": "Playing"
                }
            }
        ]
    }
}
```

---

## Admin Routes

---

/admin/<int:user_id>/give_admin/

- Methods: POST

- Arguments: user_id

- Description: Give admin permissions to a user

- Authentication: jwt_required

- Authorization: Admin only

- Request Body: none

- Response Body:

```json
{
  "message": "Success - you have given this user admin permissions."
}
```

/admin/<int:user_id>/remove_admin/

- Methods: POST

- Arguments: user_id

- Description: Remove admin permissions from a user

- Authentication: jwt_required

- Authorization: Admin only

- Request Body: none

- Response Body:

```json
{
  "message": "Success - you have removed admin permissions from this user."
}
```

/admin/all_users/

- Methods: GET

- Arguments: none

- Description: Retrieve all registered users profiles

- Authentication: jwt_required

- Authorization: Admin only

- Request Body: none

- Response Body:

```json
[
    {
        "id": 1,
        "name": null,
        "email": "admin@gametracker.com",
        "date_joined": null,
        "is_admin": true,
        "games": [],
        "notes": []
    },
    {
        "id": 2,
        "name": "Cameron Johnson",
        "email": "camjohnson@abc.com",
        "date_joined": "2020-10-10",
        "is_admin": false,
        "games": [
            {
                "title": "Red Dead Redemption 2",
                "status": "Completed"
            }
        ],
        "notes": [
            {
                "id": 1,
                "description": "This is a good game",
                "date": "2022-11-13",
                "tag": "Review",
                "game": {
                    "title": "Red Dead Redemption 2",
                    "status": "Completed"
                }
            },
            {
                "id": 3,
                "description": "On sale at JB HiFI this week",
                "date": "2022-11-13",
                "tag": "Comment",
                "game": {
                    "title": "Bayonetta 3",
                    "status": "Want to Play"
                }
            }
        ]
    },
    {
        "id": 4,
        "name": "John Smith",
        "email": "test@abc.com",
        "date_joined": "2022-11-13",
        "is_admin": false,
        "games": [],
        "notes": []
    },
    {
        "id": 3,
        "name": "James Anthony White",
        "email": "jamesanthonywhite@gmail.com",
        "date_joined": "2021-05-23",
        "is_admin": false,
        "games": [
            {
                "title": "God of War Ragnarok",
                "status": "Playing"
            },
            {
                "title": "Bayonetta 3",
                "status": "Want to Play"
            }
        ],
        "notes": [
            {
                "id": 2,
                "description": "Up to second bossfight",
                "date": "2022-11-13",
                "tag": "Progress",
                "game": {
                    "title": "God of War Ragnarok",
                    "status": "Playing"
                }
            }
        ]
    }
]
```

/admin/user/<int:user_id>/

- Methods: GET

- Arguments: user_id

- Description: Retrieve one user's profile

- Authentication: jwt_required

- Authorization: Admin only

- Request Body: none

- Response Body:

```json
{
    "id": 2,
    "name": "Cameron Johnson",
    "email": "camjohnson@abc.com",
    "date_joined": "2020-10-10",
    "is_admin": false,
    "games": [
        {
            "title": "Red Dead Redemption 2",
            "status": "Completed"
        }
    ],
    "notes": [
        {
            "id": 1,
            "description": "This is a good game",
            "date": "2022-11-13",
            "tag": "Review",
            "game": {
                "title": "Red Dead Redemption 2",
                "status": "Completed"
            }
        },
        {
            "id": 3,
            "description": "On sale at JB HiFI this week",
            "date": "2022-11-13",
            "tag": "Comment",
            "game": {
                "title": "Bayonetta 3",
                "status": "Want to Play"
            }
        }
    ]
}
```

/admin/user/<int:user_id>/

- Methods: PUT or PATCH

- Arguments: user_id

- Description: Update a user's profile

- Authentication: jwt_required

- Authorization: Admin only

- Request Body:

```json
{
    "email": "camjohnson@gmail.com",
}
```

- Response Body:

```json
{
    "message": "You have updated this user's details!",
    "user": {
        "id": 2,
        "name": "Cameron Johnson",
        "email": "camjohnson@gmail.com",
        "date_joined": "2020-10-10",
        "is_admin": false,
        "games": [
            {
                "title": "Red Dead Redemption 2",
                "status": "Completed"
            }
        ],
        "notes": [
            {
                "id": 1,
                "description": "This is a good game",
                "date": "2022-11-13",
                "tag": "Review",
                "game": {
                    "title": "Red Dead Redemption 2",
                    "status": "Completed"
                }
            },
            {
                "id": 3,
                "description": "On sale at JB HiFI this week",
                "date": "2022-11-13",
                "tag": "Comment",
                "game": {
                    "title": "Bayonetta 3",
                    "status": "Want to Play"
                }
            }
        ]
    }
}
```

/admin/user/<int:user_id>/

- Methods: DELETE

- Arguments: user_id

- Description: Delete user profile

- Authentication: jwt_required

- Authorization: Admin only

- Request Body: none

- Response Body:

```json
{
    "message": "You have successfully deleted this user.",
    "user_id": 6,
    "name": "John Smith",
    "email": "test@abc.com"
}
```

---

## Game Routes

---

/games/

- Methods: GET

- Arguments: none

- Description: Retrieve all games added to the tracker

- Authentication: none

- Authorization: none

- Request Body: none

- Response Body:

```json
[
    {
        "id": 1,
        "title": "God of War Ragnarok",
        "year_released": "2022",
        "genre": "Action",
        "platform": "PS5",
        "date_tracked": "2022-11-13",
        "status": "Playing",
        "user": {
            "name": "James Anthony White",
            "email": "jamesanthonywhite@gmail.com"
        },
        "notes": [
            {
                "id": 2,
                "description": "Up to second bossfight",
                "date": "2022-11-13",
                "tag": "Progress",
                "user": {
                    "name": "James Anthony White",
                    "email": "jamesanthonywhite@gmail.com"
                }
            }
        ]
    },
    {
        "id": 2,
        "title": "Red Dead Redemption 2",
        "year_released": "2018",
        "genre": "Action",
        "platform": "PC",
        "date_tracked": "2022-11-13",
        "status": "Completed",
        "user": {
            "name": "Cameron Johnson",
            "email": "camjohnson@gmail.com"
        },
        "notes": [
            {
                "id": 1,
                "description": "This is a good game",
                "date": "2022-11-13",
                "tag": "Review",
                "user": {
                    "name": "Cameron Johnson",
                    "email": "camjohnson@gmail.com"
                }
            }
        ]
    },
    {
        "id": 3,
        "title": "Bayonetta 3",
        "year_released": "2022",
        "genre": "Action",
        "platform": "Switch",
        "date_tracked": "2022-11-13",
        "status": "Want to Play",
        "user": {
            "name": "James Anthony White",
            "email": "jamesanthonywhite@gmail.com"
        },
        "notes": [
            {
                "id": 3,
                "description": "On sale at JB HiFI this week",
                "date": "2022-11-13",
                "tag": "Comment",
                "user": {
                    "name": "Cameron Johnson",
                    "email": "camjohnson@gmail.com"
                }
            }
        ]
    }
]
```

/games/<int:game_id>/

- Methods: GET

- Arguments: game_id

- Description: Retrieve one game from tracker

- Authentication: none

- Authorization: none

- Request Body: none

- Response Body:

```json
{
    "id": 2,
    "title": "Red Dead Redemption 2",
    "year_released": "2018",
    "genre": "Action",
    "platform": "PC",
    "date_tracked": "2022-11-13",
    "status": "Completed",
    "user": {
        "name": "Cameron Johnson",
        "email": "camjohnson@gmail.com"
    },
    "notes": [
        {
            "id": 1,
            "description": "This is a good game",
            "date": "2022-11-13",
            "tag": "Review",
            "user": {
                "name": "Cameron Johnson",
                "email": "camjohnson@gmail.com"
            }
        }
    ]
}
```

/games/

- Methods: POST

- Arguments: none

- Description: Create/add game to tracker

- Authentication: jwt_required

- Authorization: none

- Request Body:

```json
{
  "title": "Personal 5 Royal",
  "year_released": "2019",
  "genre": "RPG",
  "platform": "PS4",
  "status": "Currently Playing"
}
```

- Response Body:

```json
{
    "message": "You are now tracking Personal 5 Royal!",
    "game": {
        "id": 4,
        "title": "Personal 5 Royal",
        "year_released": "2019",
        "genre": "RPG",
        "platform": "PS4",
        "date_tracked": "2022-11-13",
        "status": "Currently Playing",
        "user": {
            "name": "James Anthony White",
            "email": "jamesanthonywhite@gmail.com"
        },
        "notes": []
    }
}
```

/games/<int:game_id>/

- Methods: PUT or PATCH

- Arguments: game_id

- Description: Update game details

- Authentication: jwt_required

- Authorization: Bearer token or Admin only

- Request Body:

```json
{
    "status": "Completed"
}
```

- Response Body:

```json
{
    "message": "You have updated the details of Personal 5 Royal!",
    "game": {
        "id": 4,
        "title": "Personal 5 Royal",
        "year_released": "2019",
        "genre": "RPG",
        "platform": "PS4",
        "date_tracked": "2022-11-13",
        "status": "Completed",
        "user": {
            "name": "James Anthony White",
            "email": "jamesanthonywhite@gmail.com"
        },
        "notes": []
    }
}
```

/games/<int:game_id>/

- Methods: DELETE

- Arguments: game_id

- Description: Delete game from tracker

- Authentication: jwt_required

- Authorization: Bearer token or Admin only

- Request Body: none

- Response Body:

```json
{
    "message": "Game \"Personal 5 Royal\" has been deleted successfully"
}
```

/games/<int:game_id>/notes/

- Methods: GET

- Arguments: game_id

- Description: Retrieve all notes on a game

- Authentication: none

- Authorization: none

- Request Body: none

- Response Body:

```json
{
    "id": 2,
    "description": "Up to second bossfight",
    "date": "2022-11-13",
    "tag": "Progress",
    "user": {
        "name": "James Anthony White",
        "email": "jamesanthonywhite@gmail.com"
    }
}
```

/games/notes/<int:note_id>/

- Methods: GET

- Arguments: note_id

- Description: Retrieve one note

- Authentication: none

- Authorization: none

- Request Body: none

- Response Body:

```json
{
    "id": 3,
    "description": "On sale at JB HiFI this week",
    "date": "2022-11-13",
    "tag": "Comment",
    "game": {
        "title": "Bayonetta 3",
        "status": "Want to Play"
    },
    "user": {
        "name": "Cameron Johnson",
        "email": "camjohnson@gmail.com"
    }
}
```

/games/<int:game_id>/notes/

- Methods: POST

- Arguments: game_id

- Description: Add a note for a tracked game

- Authentication: jwt_required

- Authorization: none

- Request Body:

```json
{
    "description": "Finish sidequest",
    "tag": "Reminder"
}
```

- Response Body:

```json
{
    "message": "You have created a note for God of War Ragnarok",
    "note": {
        "id": 4,
        "description": "Finish sidequest",
        "date": "2022-11-13",
        "tag": "Reminder",
        "user": {
            "name": "James Anthony White",
            "email": "jamesanthonywhite@gmail.com"
        }
    }
}
```

/games/notes/<int:note_id>/

- Methods: PUT or PATCH

- Arguments: note_id

- Description: Update a note

- Authentication: jwt_required

- Authorization: Bearer token or Admin only

- Request Body:

```json
{
    "description": "Finished second bossfight, up to third boss fight"
}
```

- Response Body:

```json
{
    "message": "You have updated note with id 2!",
    "note": {
        "id": 2,
        "description": "Finished second bossfight, up to third boss fight",
        "date": "2022-11-13",
        "tag": "Progress",
        "game": {
            "title": "God of War Ragnarok",
            "status": "Playing"
        },
        "user": {
            "name": "James Anthony White",
            "email": "jamesanthonywhite@gmail.com"
        }
    }
}
```

/games/notes/<int:note_id>/

- Methods: DELETE

- Arguments: note_id

- Description: Delete a note

- Authentication: jwt_required

- Authorization: Bearer token or Admin only

- Request Body: none

- Response Body:

```json
{
    "message": "This comment has been deleted."
}
```
