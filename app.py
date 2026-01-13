from flask import Flask, flash, url_for, render_template

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
        return render_template('major-plan.html')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return

@app.route("/cs-map")
def cs_map():
    try:
        return render_template('cs-map.html')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again.')
        return
    
def course_dependency():
    return render_template('course-dependency.html')

if __name__ == '__main__':
    app.debug = True
    app.run()