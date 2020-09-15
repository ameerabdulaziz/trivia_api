# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions?page=<int:page_no>'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/filtered_questions'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of question in limit 10 based on the page number
- Request Arguments: page=<page_no>
- Returns: An object with questions details 
{'success_code': 200,
'message': 'success',
'questions': questions_formatted,
'total_questions': len(questions),
'current_category': current_categories,
'categories': categories_formatted,
}

DELETE '/questions/<int:question_id>'
- Fetches a question and then delete it
- Request Arguments: None
- Returns: successs message

POST '/questions'
- Create a question
- Request Arguments: None
- Returns: The created question in a good format
{'id': id,
'question': question,
'answer': answer,
'category': category,
'difficulty': difficulty
}

POST '/filtered_questions'
- Fetch question that match the query
- Request Arguments: None
- Returns: An object with questions details 
{'success_code': 200,
'message': 'success',
'questions': questions_formatted,
'total_questions': len(questions),
'current_category': current_categories,
'categories': categories_formatted,
}

GET '/categories/<int:category_id>/questions'
- Fetch questions from specific category
- Request Arguments: None
- Returns: A list of formatted questions
[{'id': id,
'question': question,
'answer': answer,
'category': category,
'difficulty': difficulty
}]

POST '/quizzes'
- Fetch category based on the data that passed and previous questions
- Request Arguments: None
- Returns: A random question from the passed category that does not in the pervious questions in a good format
{'id': id,
'question': question,
'answer': answer,
'category': category,
'difficulty': difficulty
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```