from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, login_user
from database import db, User, register_db, ItemSignOut, Employee
import flask_login
from flask_mail import Message, Mail
import json

app = Flask(__name__)
app.secret_key = 'some_secret'
Bootstrap(app)
app.config.from_object('config')
register_db(app)

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/employeelogin')
def employeelogin():
    return render_template('employeelogin.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/logitem')
def logitem():
    return render_template('logitem.html')

@app.route('/database', methods=['GET', 'POST'])
def database():

    if request.method == 'POST':
        search = request.form.get('search')
        rows = ItemSignOut.query.filter(ItemSignOut.name.contains(search))

        return render_template("database.html", rows = rows)

    rows = ItemSignOut.query.all()
    return render_template('database.html', rows=rows)

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Invalid User')
        return render_template("logitem.html")

    elif user and password != user.query.filter_by(username=username).first().password:
        flash('Invalid Password')
        return render_template("logitem.html")

    elif user and password == user.query.filter_by(username=username).first().password:
        signature = request.form.get("signature")
        name = request.form.get("name")
        print(name)
        subtype = request.form.get("subtype")
        print(subtype)
        description = request.form.get("description")
        print(description)
        deadline = request.form.get("deadline")
        print(deadline)
        empName = request.form.get("empName")
        print(empName)
        empEmail = request.form.get("empEmail")
        print(empEmail)
        item = ItemSignOut(name, subtype, description, deadline, signature, empName, empEmail)

        db.session.add(item)
        db.session.commit()

        mail = Mail(app)
        msg = Message('Item Sign Out', sender='russellbrady456@gmail.com', recipients=[empEmail])
        msg.html = render_template("email.html", item=item)
        mail.send(msg)

        flash('Item has been logged. An Email has been sent to the borrower.')
        return render_template('homepage.html')


@app.route('/validateadmin', methods=['POST'])
def logmein():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Incorrect Username')
        return redirect('/adminlogin')

    elif user and password != user.query.filter_by(username=username).first().password:
        flash('Incorrect Password')
        return redirect('/adminlogin')

    else:
        return redirect('/database')

@app.route('/validateemployee', methods=['POST'])
def validate():
    email = request.form['email']
    password = request.form['password']
    session['email'] = email

    user = Employee.query.filter_by(email=email).first()
    if not user:
        flash('Incorrect Email')
        return redirect('/employeelogin')

    elif user and password != user.query.filter_by(email=email).first().password:
        flash('Incorrect Password')
        return redirect('/employeelogin')

    else:
        return redirect('/employeedatabase')

@app.route('/employeedatabase', methods=['GET', 'POST'])
def employeedatabase():
    email = session.get('email', None)
    if request.method == 'POST':
        search = request.form.get('search')
        rows = ItemSignOut.query.filter_by(employee_email=email).filter(ItemSignOut.name.contains(search))

        return render_template("employeeViewItem.html", rows = rows)

    rows = ItemSignOut.query.filter_by(employee_email=email)
    return render_template('employeeViewItem.html', rows=rows)

@app.route('/info', methods=['GET'])
def info():
    id = request.args.get('id')
    item = ItemSignOut.query.get(int(id))
    return render_template('signature.html', item=item)

app.run(debug=True, host='127.0.0.1')



