from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Welcome to Flask and Flask!'
users = ['mike', 'mishel', 'adel', 'keks', 'kamila']

@app.get('/users')
def users_get():
    # return 'GET /users'
	term = request.args.get('term')
	new_users = list(filter(lambda user: term in user, users))
	return render_template('users/index.html', users=new_users, search=term)

@app.route('/users/<id>')
def user_get(id):
    # return render_template('templates/users/show.html', name=id)
    return render_template('users/show.html', name=id)
    # return render_template('show.html', name=id)

@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'
