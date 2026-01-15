from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
import pandas as pd
import re

app = Flask(__name__)
app.secret_key = "temp"

def is_valid_username(s):
    return len(s) == 5 and bool(re.fullmatch(r"[A-Za-z]{2}\d{3}", s))

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if 'username' in session:
            username = session['username']
        else:
            username = None
        if request.method == 'GET':
            # If method is get, send a blank form
            if not username:
                username = None
            return render_template('index.html', user = username, page_title='Home')
        else:
            if 'login' in request.form:
                input_username = request.form.get('username')
                if is_valid_username(input_username):
                    flash(f"Welcome, {input_username}!")
                    session['username']=input_username
                    session['logged_in']=True
                    return redirect(url_for('index', user = username, page_title="Home"))
                else:
                    flash(f"Please enter a valid username.")
                    return render_template('index.html', user = username, page_title="Home")
            else:
                if username:
                    flash(f'Goodbye, {username}.')
                session['username'] = None
                return render_template('index.html', user = None, page_title="Home")
    except Exception as e:
        print(e)
        flash('An error occurred. Please try agåain.')
        return

@app.route("/major-plan")
def major_plan():
    try:
        if 'username' in session:
            username = session['username']
        else:
            username = None
        spring_df = pd.read_csv('courses/spring_courses.csv')
        all_df = pd.read_csv('courses/all_courses.csv')
        spring_with_info = spring_df.merge(
            all_df,
            on='course_tag',
            how='left'
        )
        course_info = spring_with_info.to_dict(orient='records')
        return render_template('major-plan.html', user = username, courses = course_info, page_title='Major Plan')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return

@app.route("/explore")
def explore():
    try:
        if 'username' in session:
            username = session['username']
        else:
            username = None
        if username:
            return render_template('explore.html', user = username, page_title='Explore')
        else:
            return render_template('explore.html', user = None, page_title='Explore')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return
    
def course_dependency():
    return render_template('course-dependency.html')

if __name__ == '__main__':
    app.debug = True
    app.run()