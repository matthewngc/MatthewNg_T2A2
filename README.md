# Matthew Ng - T2A2 API Webserver

---

## Link to GitHub Repository

### [GitHub Repo](https://github.com/matthewngc/MatthewNg_T2A2)

## Table of Contents

[**Installation Instructions**](#installation-instructions)

[**Purpose of this API Webserver (R1)**](#purpose-of-this-api-webserver-r1)

[**Why is it a problem that needs solving? (R2)**](#why-is-it-a-problem-that-needs-solving-r2)

[**Why this database system was chosen, and its drawbacks (R3)**](#why-this-database-system-was-chosen-and-its-drawbacks-r3)

[**Key Functionalities and Benefits of an ORM (R4)**](#key-functionalities-and-benefits-of-an-orm-r4)

[**API Endpoints (R5)**](#api-endpoints-r5)

[**Entity Relationship Diagram (R6)**](#entity-relationship-diagram-erd-r6)

[**Third Party Services & Packages Used (R7)***](#third-party-services--packages-used-r7)

[**API Webserver Models & Relationships (R8)**](#api-webserver-models--relationships-r8)

[**Database Relations Implemented (R9)**](#database-relations-implemented-r9)

[**Task Allocation & Tracking (R10)**](#task-allocation--tracking-r10)

[**References**](#references)

## Installation Instructions

---

1. Open the terminal and create a new directory

2. Move into the directory and clone this repository using the following command:

   ```git clone https://github.com/matthewngc/MatthewNg_T2A2```

3. Move into the src folder and activate a virtual environment using the following commands:

    ```python3 -m venv .venv```

    ```source .venv/bin/activate```

4. Install the required dependencies using the following command:

   ```pip install -r requirements.txt```

5. Open PostgreSQL in your terminal and create a new database named 'gametracker', a user with all access to this database, and set a password for this user

6. Open the .env file and add the details above to the DATABASE_URL using the following template, replacing {user_name} and {password} with the ones set in step 5:

    ```DATABASE_URL = postgresql+psycopg2://{user_name}:{password}@127.0.0.1:5432/gametracker```

7. Open the .flaskenv file, and set FLASK_RUN_PORT to any port that is available on your device

8. In the terminal, run the following command to create dummy objects in the database for testing purposes:

    ```flask db drop && flask db create && flask db seed```

9. In the terminal, run the following command to initialize the API webserver:

    ```flask run```

## Purpose of this API Webserver (R1)

---

The purpose of this API Webserver is to allow users to track and record the videogames that they have played, are currently playing or would like to play. Specifically, the problem to be addressed with this API application is the difficulty of managing gaming backlogs and tracking gaming progress for individuals who prefer to play multiple games at once, or like to temporarily leave games unfinished and continue at a later date.

This API application acts as a centralised hub where users can add games and include a tag to mark them as completed, currently in progress, dropped, shelved (temporarily), or plan to play, which allows them to easily track their game collection and history. Additionally, users can also add notes under each game as reviews, story progress, quest reminders and other information specific to these games. Overall, this API webserver provides an effective solution to game progress management.

## Why is it a problem that needs solving? (R2)

---

For most individuals who enjoy playing videogames, a common issue is being able to track the progress of the games they have played, particularly for those who prefer to switch between multiple games, or have commitments that make it difficult to finish a game. This leads to an excessive backlog of unfinished games, and most people may choose to give up on completing an unfinished game as they have forgotten about it, or losing interest due to a game's difficulty or a lack of an active community. This API webserver aims to not only provide a quality-of-life benefit to users to improve and enhance their gaming experience, but also create a collaborative environment for gaming communities to share their gaming experiences and history.

## Why this database system was chosen, and its drawbacks (R3)

---

This project uses the PostgreSQL database system, which is a relational database management system that supports SQL and JSON querying. This database system was chosen for the following reasons:

- PostgreSQL is ACID-compliant, meaning it has properties of atomicity, consistency, isolation and durability. Simply, it provides a high level of data validity and ensures that the data retained can be relied upon, even in cases of system errors or power failures.

- PostgreSQL is highly extensible, which means that many additional features can be added and used by the user. As such, this allows for greater levels of flexibility and freedom in terms of making complex or high level queries within the database.

- It is open source and does not require a licence to use. This also allows for a dedicated community to maintain and refine its security and reliability through bug fixes and patches.

However, some of the drawbacks with PostgreSQL relate mostly to its relational database structure, as most non-relational database management systems widely used in the industry are significantly faster in processing large amounts of data, at a lower system load. Additionally, PostgreSQL is not available by default on most computers and devices, and may require some guidance to install and use effectively.

Considering all of the above, PostgreSQL was deemed most suitable for this project mainly due to its reliability, accessibility, ease of use, and compatible nature with most ORMs. The data that will be handled in this project is predictable, small in scale, and non-complex, making PostgreSQL the best option available.

## Key Functionalities and Benefits of an ORM (R4)

---

An Object Relational Mapper (ORM) converts data stored within a relational database table into an object that can be used in object-oriented programming. By using an ORM, developers can manipulate and query a database through the use of a preferred programming language that supports object-oriented programming, and perform CRUD operations without having to directly query the database using a separate querying language.

Using this API webserver as an example, an SQL query to retrieve all records from the Games table with the id of 1 is as follows:

```sql
SELECT * FROM GAMES
WHERE game_id = 1
```

Using an ORM such as SQLAlchemy, the following Python statement can be run to recreate the same query within the database:

```python
stmt = db.select(Game).filter_by(id=1)
game = db.session.scalar(stmt)
```

By applying the above concept, a developer can easily write code to perform any complex or flexible CRUD operations on the database, which is useful in developing a web application.

Using an ORM, a developer can create a web application that can prevent users from interacting directly with the database, as it causes a significant security and privacy risk. Using an ORM to create a layer separating the user and the database, developers can control and restrict the queries that a user is able to call on a database, as well as effectively sanitising the data in order to protect the database from unwanted executable code or queries.

Additionally, the use of an ORM removes the need for boilerplate code, which increases the efficiency of the code, improves overall productivity, and minimizes the memory load of an application. Developers are also able to write code in their own preferred language, which allows the application to remain clean and consistent.

## API Endpoints (R5)

---

## Entity Relationship Diagram (ERD) (R6)

---

![ERD](docs/erd.png)

## Third Party Services & Packages Used (R7)

---

This projects utilises the following third party services and PyPI packages:

- Flask-SQLAlchemy
  
  - SQLAlchemy is an SQL tookit and ORM written in Python that allows users to convert data from a relational database to Python objects. Flask-SQLAlchemy is an extension of Flask that provides support for SQLAlchemy in a Flask application. Flask-SQLAlchemy is used in this project to map tables from the database to a Python class object model, which can then be used to create, read, update and delete tables in the database.

- Flask

  - Flask is a web microframework that is used to create and develop web applications in Python. Flask allows users to easily build a simple web application in a single Python file, and does not require a specific directory structure, hence it is highly extensible. Flask is used in this project to set up the framework of the web application, and create routes that can receive web requests and send responses.

- Marshmallow

  - Marshmallow is an ORM library that allows the conversion of complex datatypes and objects to and from Python datatypes. Marshmallow can also be used to validate input data. Flask-Marshmallow is an extension to Flask that integrates Marshmallow with the Flask microframework. In this project, Marshmallow is used to transform JSON inputs into Python objects, as well as converting Python objects into valid JSON outputs. It is also used for data validation, where certain input fields must conform to a specified constraint.

- Bcrypt

  - Bcrypt is a password-hashing function that is used to encrypt passwords before it is stored in the database. A password string is hashed, meaning it is passed through an algorithm to map it to an encrypted string. A fixed length random value known as a salt is added to each hash in order to create a unique hash for every password. This unique salt value is used to decrypt the password hashes stored within the database for the purposes of authentication. Flask-Bcrypt is an extension to Flask that incorporates the Bcrypt function within a web application. For this project, Flask-Bcrypt is used primarily for the purposes of password encryption and user authentication.

- Flask-JWT-Extended

  - Flask-JWT-Extended is a Flask extension that provides support to Flask for using JWT tokens in order to protect routes in the framework. A JWT token is generated upon user login, and is included with every subsequent request made by the user to the server in order to authenticate their identity. This can also be used for the purposes of authorization, such as verifying administrator privileges before the web application returns a response to a request. For this project, Flask-JWT-Extended is used to protect routes by ensuring that the user must be logged in to make certain requests, as well as verifying administrator privileges in order to access admin-only routes.

- psycopg2

  - Psycopg is a PostgreSQL database adapter for the Python programming language. It is widely used in multi-threaded applications that handles a large number of create and delete operations, and concurrent insert or update operations to a PostgreSQL database. For this project, Psycopg was used to connect the Flask application to the PostgreSQL database, in order for the application to perform queries and operations on the database.

- Python-dotenv

  - Python-dotenv is a Python package that loads environment variables from a .env file into a Python module. For this project, Python-dotenv was used to retrieve values from a .flaskenv and .env file in order to configure the application. Variables are loaded from the .flaskenv file in order to configure the Flask application by specifying the Python file to run, activate the debugger and specify the server port the application will be running on. For sensitive information such as the database URL and the JWT secret key, the variables are loaded from the .env file.

- Other dependencies

  - There are additional dependencies that will be installed when installing the packages listed above. All packages and dependencies required for this API application have been frozen in the [requirements.txt](src/requirements.txt) file.

## API Webserver Models & Relationships (R8)

---

For this API project, the database entities are represented by three SQLAlchemy models. To generate these models, the base class db.Model is used, and Fields representing the attributes of each entity are added to the base class. The relationships between each model is then represented through the use of foreign key attributes within each model.

The three models in this project are the User model, Game model and Note model.

### **User Model**

The User model in this API application represents the users that are registered on the database. While the User model does not have a foreign key relating to other models, the other two models have foreign keys that reference the User model. This represents a one-to-many relationship between the User model and the Game and Note models.

```python
games = db.relationship('Game', back_populates = 'user', cascade = 'all, delete')
notes = db.relationship('Note', back_populates = 'user', cascade = 'all, delete')
```

The above code snippet shows the relationship between the User model and the other two models. While the User model does not have any foreign key attributes, it is referenced by the other two models in their respective foreign key attributes. As such, the db.relationship() function establishes this bidirectional relationship, where the back_populates parameter connects the two models together. The cascade parameter specifies that if a user is deleted from the database, all related games and notes tied to this user will also be deleted accordingly.

### **Game Model**

The Game model in this API represents the games that a user has added to the database to track. Each user can add many games to the database, however each game that is added to the tracker can only be designated to one user. As such, this is a one-to-many relationship that is represented in the following code snippet:

```python
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

user = db.relationship('User', back_populates='games')
```

The first line of the code snippet defines the foreign key attribute within the Game model that links to the User model. The db.Column function is used to define the parameters of an attribute, and the db.ForeignKey parameter declares this attribute as the foreign key relating to the Users model. The nullable parameter designates that each foreign key must correspond to a primary key id in the associated model. The second line of the snippet completes the relationship established in the User model.

The Game model is also referenced by the foreign key attributes within the Note model. Similarly to the User model, the relationship is established through the following line:

```python
notes = db.relationship('Note', back_populates='game', cascade = 'all, delete')
```

### **Note Model**

The Note model represents the notes that a user can add to their tracked games. As such, notes have a many-to-one relationship with both a user and a game, and have foreign keys that reference the User model and Game model.

```python
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable = False)

user = db.relationship('User', back_populates='notes')
game = db.relationship('Game', back_populates='notes')
```

As established for the other models, the above snippets completes the associations between the Note model and the User and Game models.

## Database Relations Implemented (R9)

---

The database relations of this API application is visualised using the [Entity Relationship Diagram](#entity-relationship-diagram-erd-r6). The three entities depicted within the diagram represent the tables in the database.

Each table has a primary key that is uniquely assigned to each record in the table. A table can have an attribute known as a foreign key that references another table's primary key. This is what will establish associations between each entity.

Using the ERD as an example, the games table has an attribute named user_id (foreign key) which corresponds with an id (primary key) in the users table. This means that for each record in the games table, it is directly related to one unique user. This is the basis on which the three tables in the ERD are linked.

In the ERD, the relations between each entity is represented through the crow's foot notation connecting the primary keys and the foreign keys. In layman's terms, the relationships between the three entities are as follows:

- A user can add none or many games to the tracker, however a game that has been added to the tracker is only associated with one user. As such, users have a zero or many relationship with games, while a game has a one and only one relationship with a user.
  
- A user can add none or many notes to a game, however a note that has been added to a game is only associated with one user. As such, users have a zero or many relationship with notes, while a note has a only and only one relationship with a user.

- A game can have none or many notes added to it, however a note that has been added to a game is only associated with one game. As such, games have a zero or many relationship with notes, while a note has a one and only one relationship with a game.

## Task Allocation & Tracking (R10)

---

[Link to Trello Board](https://trello.com/invite/b/Q4vCldYy/ATTI539bc741fc769e94128abb448f1fb7e288AF73A9/t2a2-api-webserver-project)

To manage tracking and allocation of tasks, Trello was used for this project. After creating a board, four lists were created for the different stages of each component of the project: 'To Do', 'Ongoing', 'Testing' and 'Done'. Labels were also created for priority ('Low', 'Medium', 'High'), as well as the nature of the task ('Planning', 'Coding', 'Documentation').

After the Trello board is set up, the project is broken up into segments that are then converted into cards. Within each individual card, the appropriate labels and due dates are assigned, and a checklist is added to the card to outline the steps required for the particular segment. For example, to develop the game controller, a checklist was made for each route that is required to complete the CRUD operations:

- GET route: read all games

- GET route: read one game

- POST route: create a new game

- PUT/PATCH route: update game details

- DELETE route: delete a game

After all the cards are created, they are added to the board in the 'To Do' list. Once work begins on a card, it is moved to the 'Ongoing' queue, where the checklist is worked through. Once complete, the card is moved to the 'Testing' list, where the code that relates to that segment is checked and tested using Postman and dummy objects. If the test results are not satisfactory, it moves back into the 'Ongoing' queue, otherwise it is moved to the 'Done' list.

![trello_board](docs/trello.PNG)

## References

---

Amazon Web Services. (n.d.) What is PostgreSQL? Retrieved November 11, 2022 from [https://aws.amazon.com/rds/postgresql/what-is-postgresql/](https://aws.amazon.com/rds/postgresql/what-is-postgresql/)

Flask SQLAlchemy. (n.d.). Models and Tables. Retrieved November 11, 2022 from [https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/)

Dyouri, A. (2022, March 10). How to Use Flask-SQLAlchemy to Interact with Database in a Flask Application. DigitalOcean. Retrieved November 12, 2022 from [https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)

Makai, M. (2022). Object-relational Mappers (ORMs). Full Stack Python. Retrieved November 13, 2022 from [https://www.fullstackpython.com/object-relational-mappers-orms.html](https://www.fullstackpython.com/object-relational-mappers-orms.html)

Liang, M. (2021, March 11). Understandinng Object-Relational Mapping: Pros, Cons, and Types. altexsoft. Retrieved November 13, 2022 from [https://www.altexsoft.com/blog/object-relational-mapping/](https://www.altexsoft.com/blog/object-relational-mapping/)

Hoyos, M. (2018, December 25). What is an ORM and Why You Should Use it. Medium. Retrieved November 13, 2022 from [https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a](
https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a)

SQLAlchemy. (n.d.). The Python SQL Toolkit and Object Relational Mapper. Retrieved November 13, 2022 from [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)


Marshmallow. (n.d.). marshmallow: simplified object serialization. Retrieved November 13, 2022 from [https://marshmallow.readthedocs.io/en/stable/](https://marshmallow.readthedocs.io/en/stable/)

JWT. (n.d.). Introduction to JSON Web Tokens. Retrieved November 13, 2022 from [https://jwt.io/introduction](https://jwt.io/introduction)


Gupta, C. (2022, June 3). Hashing Passwords in Python with BCrypt. GeeksForGeeks. Retrieved November 13, 2022 from [https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/](https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/)