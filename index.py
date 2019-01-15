import pprint
from flask import Flask, session
from flask import render_template, redirect, request, url_for, abort, session
from flask_test.models import models

app = Flask(__name__)

app.secret_key = b'ycbe0wf4yb974w8y7bf54gerwov7678ct'

# NAMES for task 2
names = []
# boxes
boxes = {"red": {"red_box": {"item1": 3, "item2": 1}}, "green": {}, "blue": {}, "yellow": {}, "magenta": {}}

user_boxes = {"red": {"red_box": 'admin'}, "green": {}, "blue": {}, "yellow": {}, "magenta": {}}

user_auth = {'admin': 'top_secret', 'ryo': 'qwerty'}

from functools import wraps
from flask import Response


# is user authenticated
def require_authentication(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if session.get('username') in user_auth:
            return fn(*args, **kwargs)
        else:
            return render_template('index.html'), 403

    return decorated


@app.route('/getuser')
def test():
    user = models.User.get(username='admin')
    return str(user.created_at)


# is user authenticated
def is_authorized(color, name, username):
    return user_boxes.get(color).get(name) == username


@app.route('/')
def hello_world():
    return render_template('index.html', username=session.get('username'))


@app.route('/task')
@app.route('/task/<int:count>', methods=['GET', 'POST'])
def tasks(count=None):
    if count is None or count < 2 or count > 5 :
        return redirect('/')

    name = request.args.get('name')
    if name is not None and request.method == 'POST':
        names.append(name)

    return render_template('task.html', count=count, names=names)


@app.route('/boxes', methods=['GET', 'POST'])
@require_authentication
def my_boxes():
    error = ''
    name = request.args.get('name')
    color = request.args.get('color')
    if request.method == 'POST':
        if color in boxes and name is not None:
            box = boxes.get(color).get(name)
            if box is None:
                boxes[color][name] = {}
                user_boxes[color][name] = session.get('username')
            else:
                error = 'Box is already exists!'
        elif color not in boxes:
            error = 'Color is wrong or not defined!'
        elif name is None:
            error = 'Name is not defined!'

    return render_template('boxes.html', boxes=boxes, error=error)


@app.route('/boxes/<color>/<name>', methods=['GET', 'POST'])
@require_authentication
def my_box(color, name):
    if boxes.get(color).get(name) is None:
        abort(404)

    box = boxes[color][name]

    if request.method == 'POST':
        if not is_authorized(color, name, session.get('username')):
            abort(403)
        item = request.args.get('item')
        if item is not None:
            if item in box:
                box[item] += 1
            else:
                box[item] = 1

    return render_template('box.html', box=box, color=color, name=name)


@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username is None or password is None:
        return render_template('index.html', message='Please, set both username and password.'), 400

    user = models.User.get(models.User.username == username and models.User.password_hash == hash(password))

    if user is not None:
        session['username'] = user.username
        return render_template('index.html', username=username), 200

    return render_template('index.html'), 403


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/')


@app.route('/hash/<string:password>')
def get_hash(password):
    return str(hash(password))