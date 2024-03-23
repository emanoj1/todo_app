## To Do App ##
This is a coding study project utilizing Python, Flask, SQLAlchemy and PostgreSQL. It's main purpose is to provide users with a simple platform for creating, updating, and tracking their tasks or to-do items.  

In this project, we aim to perform and check these 3 tasks only:
<ol>
<li>CRUD - Create, delete, update and view tasks</li>
<li>user authentication (user registration and login)</li>
<li>API Routes</li>
</ol>

### Installation and Testing ###

1. Fork the repository on your system
2. Open it in a code editor like VS Code
3. You will now see these files: models.py, auth.py, main.py, blueprints.py, controllers.py and requirements.txt
   
4. The application has the function to check if you have a virtual environment (.venv) and if not, create one for you. If you want to create the virtual environment yourself, type the below command in your coding terminal:
	- `python3 -m venv .venv`
	- `source .venv/bin/activate (MacOS)` or `.venv/Scripts/activate`
	  
5. The source code also has the function to check and install dependencies if required. If you want to create it yourself, type the below command:
	- `pip install -r requirements.txt`
	- `pip freeze > requirements.txt`

6. Create a `env` file in your terminal
7. Use these variables in the `env` file:
		DATABASE_URI=
		JWT_SECRET_KEY=

6.  Make sure PostgreSQL installed on your system ELSE install from here: https://www.postgresql.org/download/

7.  Assign your PostgeSQL credentials to the database.

8. Configure your database. _Example below:_
	**CREATE DATABASE todo_db;**
	CREATE USER todo_dev WITH PASSWORD '12345';

9. Configure a Category database.
	**CREATE DATABASE category;

10. Seed values into the Category database
	**INSERT INTO category (name) VALUES ('a_category_name');**

These categories are pre-defined, and the user chooses one of them when creating new to-dos.
_Examples:_
`INSERT INTO category (name) VALUES ('Home');`  
`INSERT INTO category (name) VALUES ('Holiday');`  
`INSERT INTO category (name) VALUES ('Bills');`  

11. Run these commands to create the models:
		`flask db init`  
		`flask db migrate`  
		`flask db upgrade`  

12. Execute the application:  
		`flask run`

13. Testing API Endpoints
	1. Use Insomnia/Postman. 
	2. The JSON script examples are provided below.
	3. Use http://localhost:8000/  

<hr style="border:2px solid gray">

<h1>API Route Testing</h1>

Below are the API endpoints for this app:

## User Registration ##
   - Endpoint: `/signup`
   - Method: `POST`

<span style="color:blue">Example JSON code for testing</span>  
`{`  
`"username":"john doe"`,  
`"password":"TeST123!"`  
`}`

## User Login ##
   - Endpoint: `/login`
   - Method: `POST`  

<span style="color:blue">Example JSON code for testing</span>  
`{`  
`"username":"john doe"`,  
`"password":"TeST123!"`  
`}`

## Create a Todo ##
   - Endpoint: `/api/todos`
   - Method: `POST`
   - Description: Creates a new todo item.

<span style="color:blue">Example JSON code for testing</span>  
`{`   
`"title": "Pay Bills",`  
`"description": "Electricity, Health Insurance, Traffic fine",`  
`"due_date": "2024-03-20",`  
`"completed": false,`  
`"user_id": 1,`  
`"category_id": 1,`  
`"tags": ["monthly"]`  
`}`

## Retrieve ALL Todos ##
   - Endpoint: `/api/todos`
   - Method: `GET`

<span style="color:blue">Example JSON code for testing</span>
- NONE
- Use only the HTTP request below with the GET method.

 > **HTTP request URL**: http://localhost:8000/api/todos

 ## Retrieve a SINGLE/SPECIFIC Todo item
   - Endpoint: `/api/todos/<todo_id>`
   - Method: `GET`

<span style="color:blue">Example JSON code for testing</span>
- NONE
- Use the below HTTP request with the specific todo_id (integer) mentioned at the end

 > **HTTP request URL**: http://localhost:8000/api/todos/<todo id>

 ## Retrieve items of a specific tag ##
   - Endpoint: `/api/tag/<tag_name>/todos`
   - Method: `GET`

<span style="color:blue">Example JSON code for testing</span>
- NONE
- Use the below HTTP request format containing the tag route and the tag name.

> **HTTP request URL**: http://127.0.0.1:8000/api/tag/gifts/todos

## Update a Todo ##
   - Endpoint: `/api/todos/<todo_id>`
   - Method: `PUT`

<span style="color:blue">Example JSON code for testing</span>
`{`  
`"title": "Example Todo",`  
`"description": "This is a test todo item 2",`  
`"due_date": "2024-03-20",`  
`"completed": false,`  
`"user_id": 1,`  
`"category_id": 1,`  
`"tags": ["monthly"]`  
`}`

> **HTTP request URL**: http://localhost:8000/api/todos

## Delete Todo Endpoint ##
   - Endpoint: `/api/todos/<todo_id>`
   - Method: `DELETE`

<span style="color:blue">Example JSON code for testing</span>
- Not required. Only the request verb with the todo_id is required along with the DELETE method.

> **HTTP request URL**: http://127.0.0.1:8000/api/todos/1

<hr style="border:2px solid gray">

## Database Relationship ##

1. **User**:
     - One-to-Many with `TodoItem`: Each user can have multiple todo items associated with them.
     - One-to-Many with `Tag`: Each user can have multiple tags associated with them.
   
2. **TodoItem**:
     - Many-to-One with `User`: Each todo item belongs to a single user.
     - Many-to-One with `Category`: Each todo item belongs to a single category.
     - One-to-Many with `Tag`: Each todo item can have multiple tags associated with it.
   
3. **Category**:
     - One-to-Many with `TodoItem`: Each category can have multiple todo items associated with it.

4. **Tag**:
     - Many-to-One with `User`: Each tag belongs to a single user.
     - Many-to-One with `TodoItem`: Each tag belongs to a single todo item.

<hr style="border:2px solid gray">

Thank you for checking out this project.