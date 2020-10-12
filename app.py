from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#this is telling our app where our database is located
#four forward slashes is an absolute path
#three forward slashes is a relative path
#using three here so we don't have to specify exact location, just reside in project location
#we'll call the database 'test.db', everything will be stored here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#initialize our database
#database is being initialized with the settings from our app
db = SQLAlchemy(app)

#now we need to create a model
class Todo(db.Model):
	#setting up our columns
	#first is id column, integer that references id of each entry
	id = db.Column(db.Integer, primary_key=True)

	#let's create a text column
	#in our case, this will hold each task
	#nullable set to false so user won't be able to create new task and leave the content empty
	content = db.Column(db.String(200), nullable=False)

	#for time, don't forget to import datetime
	#this will always be set automatically
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	#we want a function that returns a string everytime we create a new element
	#so everytime we create a new element, it will return the idea of that task that was created
	def __repr__(self):
		return '<Task %r>' % self.id

#to import our database into the interactive shell, we can type from app import db
#use db.create_all() to create our database 'test.db'
#now our database should be setup

#create an index route so that when we browse 
#into the URL, we don't 404 right away
#setup routes with @app.route decorator 
#you can also add two methods that this route can accept
#now instead of just GET by default, we can POST to this route as well and send data to our db
@app.route('/', methods=['POST', 'GET'])
def index():
	#don't forget to import request
	if request.method == 'POST':
		#create a new task from our input
		#form for the form we created, and pass in id of the input we want to get the content of
		task_content = request.form['content']

		#Todo model object who's contents will be equal to the contents of the input
		new_task = Todo(content=task_content)

		#now push to the database
		try:
			#add to the database session
			db.session.add(new_task)

			#commit to database
			db.session.commit()

			#return redirect back to index page, don't forget to import redirect
			return redirect('/')
		except:
			return 'There was an issue adding your task'
	else:
		#this will look at all of the database contents in the order that they were created
		#and return all of them
		#can also do .first() to grab the first, which would be the most recent if sorting by date
		tasks = Todo.query.order_by(Todo.date_created).all()

		#don't have to specify 'template' folder
		#function knows where to look
		#pass tasks into template, tasks=tasks
		return render_template('index.html', tasks=tasks)

#we have CREATE done from CRUD now, let's do DELETE
#use id to identify unique task, id will always be unique
@app.route('/delete/<int:id>')
def delete(id):
	#create a variable for the task to delete
	#query database, then attempt to get task by id and if doesn't exist, 404 error
	task_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return 'There was a problem deleting that task'

#now let's do UPDATE from CRUD
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	task = Todo.query.get_or_404(id)

	if request.method == 'POST':
		#we are setting the current task's content to the content in the update form's input box
		task.content = request.form['content']

		try:
			#just need to commit because we set the content in the previous line, just updating
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue updating your task'
	else:
		return render_template('update.html', task=task)

if __name__ == "__main__":
	#if we have any errors they will popup on webpage
	app.run(debug=True)


#to run server: python3 app.py

#use source env/bin/activate to activate virtual environment

#template inheritance:
#you create one master html file that contains the skeleton of what each page will look like
#and then you just inherit that in each other page and insert code when needed
#so you only have to write what is relevant

#{% block head %}{% endblock %}
#this is Jinja2 syntax
#Jinja is the template engine Flask uses
#we are creating a block template, and this is where we insert our own code
#on all of the other pages that inherit this template
#{% %} is for stuff like if else statements, for loops, etc.
#{{ }} these are for things you want to be printed as strings
#it will take you write in {{ }} and give you the result of that as a string
#need to use a function url_for, import first
#flow for linking the stylesheet is similar for JavaScript

#gunicorn creates a webserver, and need to tell Procfile what file to create a web server for
