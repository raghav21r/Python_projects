from flask import Flask, render_template, request, redirect,flash,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import time
import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import docker
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///details.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key=os.urandom(24)
database = SQLAlchemy(app)

isolated_env=docker.from_env()

class MyFirstApp(database.Model):
    Your_url = database.Column(database.String(300), nullable=False)
    
    Password = database.Column(database.String(300), nullable=False)
    email_id=database.Column(database.String(300),nullable=False)
    id=database.Column(database.Integer,primary_key=True,autoincrement=True)


def user_is_present(mailid):
    existing_user = MyFirstApp.query.filter_by(email_id=mailid).all()
    return existing_user
def in_the_database(password_input):
    is_present=MyFirstApp.query.filter_by(Password=password_input).first()
    return is_present
def in_the_server(mailid):
    is_present=MyFirstApp.query.filter_by(email_id=mailid).first()
    return is_present
@app.route('/', methods=['GET', 'POST'])
def function1():
    if request.method == 'POST':
        Your_url = request.form.get('Your_url', '')  # Get URL from form
        Password = request.form.get('Password', '')  # Get password from form
        mail=request.form.get('email_id','')
        if Your_url and Password and mail:
            details_are_available=user_is_present(mail)
            if details_are_available:    
                info = MyFirstApp(Your_url=Your_url, Password=Password,email_id=mail)
                database.session.add(info)
                database.session.commit()
                return redirect(url_for('function2',record_id=info.id))
            else:
                info = MyFirstApp(Your_url=Your_url, Password=Password,email_id=mail)
                database.session.add(info)
                database.session.commit()
                return redirect(url_for('function2',record_id=info.id))
    # Get all records to display
    build = MyFirstApp.query.all()
    return render_template("second.html",build=build)
@app.route('/history',methods=['GET','POST'])
def history():
    Password = request.form.get('Password', '')
    # Get all records to display
    build = MyFirstApp.query.all()
    return render_template('history.html', build=build)

@app.route('/delete/<int:id>')
def delete(id):
    remove=MyFirstApp.query.filter_by(id=id).first()
    database.session.delete(remove)
    database.session.commit()
    return redirect("/history")

@app.route('/options/<int:record_id>',methods=['GET','POST'])
def function2(record_id):
    dataset = MyFirstApp.query.get(record_id)
    if not dataset:
        flash("Record not found", "error")
        return redirect('/')
    
    Your_url = dataset.Your_url
    # Protocol Check
    if not Your_url.startswith(('http://', 'https://')):
        Your_url = 'http://' + Your_url
    choices = Options()
    choices.add_argument('--no-sandbox')  # Fixed typo: was '--no sandbox'
    choices.add_argument('--disable-dev-shm-usage')
    container_name=f"safe_env{record_id}"
    try:
        predefined_container=isolated_env.containers.get(container_name)
        predefined_container.stop()
        predefined_container.remove()
    except:
        pass
    # Docker Execution for Isolation
    isolated_env.containers.run(
        'selenium/standalone-chrome:latest',
        detach=True,
        ports={'4444/tcp':4444, '7900/tcp':8080},
        environment={'SE_VNC_NO_PASSWORD': '1'},
        shm_size='2g',
        name=f'Safe_env{record_id}',
        remove=True
    )
    
    # Give container time to start - MOVED HERE
    time.sleep(10)  # Increased to 10 seconds for reliability
    
    
    
    try:
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=choices
        )
        driver.get(Your_url)
    except Exception as e:
        return f"Error launching browser: {str(e)}"
    
    return f'''
    <html>
    <body>
        <h2>Browser running for: {Your_url}</h2>
        <p>Open browser view: <a href="http://localhost:8080" target="_blank">http://localhost:8080</a></p>
        <iframe src="http://localhost:8080" width="100%" height="800px"></iframe>
    </body>
    </html>
    '''
if __name__ == '__main__':
    # Create tables within application context
    with app.app_context():
        database.create_all()
        print("Database tables created successfully!")
    
    # Run the app
    app.run(debug=True)
