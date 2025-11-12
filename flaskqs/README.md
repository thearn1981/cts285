# Flask Quick Start Assignment
I decided to use visual studio code and pull my repo from git hub.
So the following is for the visual studio code terminal.

## Setting the Virtual environment

to change directory:
cd flaskqs

to create the venv folder:
py -m venv env  
(-m stands for module)

to activate the environment:
env\Scripts\activate 
(this is for visual studio code)

## Flask installation
py -m pip install flask

## check flask version
flask --version

## create requirements.txt
pip freeze > requirements.txt

## Beginning the quick start

### to run flask
flask --app hello run

#### To make it externally visible
flask --app hello run --host=0.0.0.0  

#### To turn debug on
flask --app hello run --debug

#### To help against injection attacks.
import escape

#### proper file structure 
Having proper file structure is important when working with flask in reguards to having 
templates and static files that will be used when displaying different pages for the application.

#### When doing testing
after tests code during develop is important. Making sure modules only run when called and If statements only activate when
the condition are met is important. 
once you have created and ready to run the tests. running the test from the right folder is important.
OR you could create a pip install for the flaskr so that the tests will work properly.

