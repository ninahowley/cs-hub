from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
import pandas as pd
import re
import db_functions as db
import json

app = Flask(__name__)
app.secret_key = "temp"

def is_valid_username(s):
    return len(s) == 5 and bool(re.fullmatch(r"[A-Za-z]{2}\d{3}", s))

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        spring_df = pd.read_csv('courses/spring_courses.csv')
        all_df = pd.read_csv('courses/all_courses.csv')
        spring_with_info = spring_df.merge(
            all_df,
            on='course_tag',
            how='left'
        )
        spring_course_info = spring_with_info.to_dict(orient='records')
        with open('static/spring_courses.json', 'r') as file:
            spring_dict = json.load(file)
        if 'username' in session:
            username = session['username']
        else:
            username = None
        if request.method == 'GET':
            # If method is get, send a blank form
            if not username:
                username = None
            return render_template('index.html', user = username, spring_courses = spring_course_info, page_title='Home')
        else:
            if 'login' in request.form:
                input_username = request.form.get('username')
                if is_valid_username(input_username):
                    flash(f"Welcome, {input_username}!")
                    session['username']=input_username
                    session['logged_in']=True
                    return redirect(url_for('index', user = username, spring_courses = spring_course_info, page_title="Home"))
                else:
                    flash(f"Please enter a valid username.")
                    return render_template(
                        'index.html', 
                        user = username, 
                        spring_courses = spring_course_info,
                        spring_data = spring_dict, 
                        page_title="Home")
            else:
                if username:
                    flash(f'Goodbye, {username}.')
                session['username'] = None
                return render_template(
                    'index.html', 
                    user = None, 
                    spring_courses = spring_course_info, 
                    spring_data = spring_dict,
                    page_title="Home")
    except Exception as e:
        print(e)
        flash('An error occurred. Please try agåain.')
        return

def get_remaining_courses(username: str):
    courses_taken = db.get_user_courses(username)
    core_courses = ["CS 111", "CS 112", "CS 230", "CS 231", "CS 235", "CS 240"]
    cores_taken = [course for course in courses_taken if course in core_courses]
    cores_not_taken = [course for course in core_courses if course not in courses_taken]
    if "CS 111" in cores_taken:
        cores_not_taken.remove("CS 112")
    if "CS 112" in cores_taken:
        cores_not_taken.remove("CS 111")
    electives_taken = [course for course in courses_taken if course not in core_courses and course[3] in ["2", "3"]]
    electives_remaining = 0
    if len(electives_taken) < 4:
        electives_remaining = 4 - len(electives_taken)
    level_300s = len([course for course in electives_taken if course[3] == "3"])
    remaining_300s = 0
    if level_300s < 2:
        remaining_300s = 2 - level_300s
    remaining_dict = {
        "num_cores_remaining": len(cores_not_taken),
        "cores_remaining": ', '.join(cores_not_taken),
        "electives_remaining": electives_remaining,
        "level_300s": remaining_300s
    }
    return remaining_dict

@app.route("/major-plan")
def major_plan():
    try:
        #display all courses
        all_df = pd.read_csv('courses/all_courses.csv')
        all_course_info = all_df.to_dict(orient='records')
        elective_df = all_df[all_df["course_core"] == False] #remove core
        elective_info = elective_df.to_dict(orient='records')

        if 'username' in session:
            username = session['username']
            #display user courses
            remaining_info = get_remaining_courses(username)
            taken_courses = db.get_user_courses(username)
            taken_courses = [course.strip() for course in taken_courses]
            taken_electives_df = elective_df[elective_df["course_tag"].isin(taken_courses)] #only keep taken
            taken_electives = taken_electives_df.to_dict(orient='records')
        else:
            username = None
            taken_electives = []
        
        #display spring courses
        spring_df = pd.read_csv('courses/spring_courses.csv')
        spring_with_info = spring_df.merge(
            all_df,
            on='course_tag',
            how='left'
        )
        spring_course_info = spring_with_info.to_dict(orient='records')
        return render_template(
            'major-plan.html', 
            user = username, 
            all_courses = all_course_info, 
            taken_courses = taken_courses,
            taken_electives = taken_electives, 
            electives = elective_info, 
            remaining_info = remaining_info,
            page_title='Major Plan'
        )
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return

@app.route("/add-course", methods=['POST'])
def add_course():
    if 'username' not in session:
        flash('not logged in.')
        return redirect(url_for('major_plan'))
    
    username = session['username']
    course_code = request.form.get('course_code')
    is_core = request.form.get('is_core')
    
    if not course_code:
        flash('not a valid course code')
        return redirect(url_for('major_plan'))
    try:
        print("got to try")
        db.upload_registration(username, course_code)
    except Exception as e:
        print(e)
        flash('error uploading to db.')
    return redirect(url_for('major_plan'))

@app.route("/drop-course", methods=['POST'])
def drop_course():
    if 'username' not in session:
        flash('not logged in.')
        return redirect(url_for('major_plan'))
    
    username = session['username']
    course_code = request.form.get('course_code')
    is_core = request.form.get('is_core')
    
    if not course_code:
        flash('not a valid course code')
        return redirect(url_for('major_plan'))
    try:
        print("got to try")
        db.delete_registration(username, course_code)
    except Exception as e:
        print(e)
        flash('error uploading to db.')
    return redirect(url_for('major_plan'))

@app.route("/explore")
def explore():
    try:
        # load data from explore.json to fill in the explore page
        # edit explore.json to display data
        with open('static/explore.json', 'r') as file:
            explore_dict = json.load(file)
        if 'username' in session:
            username = session['username']
        else:
            username = None
        if username:
            return render_template('explore.html', user = username, data = explore_dict, page_title='Explore')
        else:
            return render_template('explore.html', user = None, data = explore_dict, page_title='Explore')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return
    
def course_dependency():
    return render_template('course-dependency.html')

if __name__ == '__main__':
    app.debug = True
    app.run()