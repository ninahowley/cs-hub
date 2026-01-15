from flask import Flask, flash, url_for, render_template
import pandas as pd

app = Flask(__name__)
app.secret_key = "temp"

@app.route("/")
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try agåain.')
        return

@app.route("/major-plan")
def major_plan():
    try:
        spring_df = pd.read_csv('courses/spring_courses.csv')
        all_df = pd.read_csv('courses/all_courses.csv')
        spring_with_info = spring_df.merge(
            all_df,
            on='course_tag',
            how='left'
        )
        course_info = spring_with_info.to_dict(orient='records')
        return render_template('major-plan.html', courses = course_info)
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return

@app.route("/explore")
def explore():
    try:
        return render_template('explore.html')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return
    
def course_dependency():
    return render_template('course-dependency.html')

if __name__ == '__main__':
    app.debug = True
    app.run()