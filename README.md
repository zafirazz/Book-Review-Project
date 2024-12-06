# Project Title

A website where users can write and read reviews for books.

## Getting Started
This website is run using Pycharm professional Edition.
In order to get the website running, check requirements.txt.

### Installing

After downloading the necessary requirements and opening this project on Pycharm, click on the database tab on the right and connect to postgresSQL

<img alt="img.png" height="200" src="images/img.png" width="400"/>

if you choose the "No auth" option, running login.py should be successful. <br>
if you choose the "User & Password" option, add your username and password to the database settings, and add your username and password in the create_engine as shown below.

_*!!make sure to uncomment engine = create engine(...)!!*_
```
#engine = create_engine('postgresql+psycopg2://username:password@localhost:5432/postgres')

app = Flask(__name__, template_folder='front-end', static_folder='front-end/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost:5432/postgres'
app.secret_key=["hioergerhgoierhgierhogiehgoieagawoeigyireyg"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```
After inserting your username and password in the engine details, change the url in app.config as follows:
```
engine = create_engine('postgresql+psycopg2://username:password@localhost:5432/postgres')

app = Flask(__name__, template_folder='front-end', static_folder='front-end/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://username:password@localhost:5432/postgres'
app.secret_key=["hioergerhgoierhgierhogiehgoieagawoeigyireyg"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

Running login.py should present the following output in the terminal:

![img_1.png](images/img_1.png)

### Working With The Website

Accessing the provided link from the terminal and adding "front-end/[write into the url any html file found in front-end directory]"

Examples:
<br>
http://127.0.0.1:5000/front-end/home

<img alt="img_3.png" height="200" src="images/img_3.png" width="400"/>


http://127.0.0.1:5000/front-end/search

<img alt="img_2.png" height="200" src="images/img_2.png" width="400"/>

### Key Features
* Users will see a main interface featuring a user-friendly design with book covers and essential information about the website.
* They will also have options to Register or Login, allowing access to additional features.
* A **Search** button will be available, enabling users to search for books.
* Clicking the **Register** option directs users to the registration page, while the **Login** option leads to the login page.
* Clicking on the **Review** option will allow the user to either read reviews, or write reviews.
* Only logged-in users can write reviews.
* The website's user interface will incorporate cohesive branding, including logos and a consistent color scheme.



