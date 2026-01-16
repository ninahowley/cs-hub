# Wellesley CS Hub

CS Hub is a website where Wellesley CS majors and other students interested in CS can view course offerings, plan their major and explore the many fields of CS. It was made for the UpSkill: Software Development Lifecycle program.

## How to Use

<h3>Home Page<h3>
Enter your Wellesley ID in the **Login** section on the **Home Page** (or any username you want).
<img alt="image" src="static/screenshots/home.png" />

<h3>Major Plan<h3>
Check your CS major plan in the **Major Plan** page and explore all CS course options at Wellesley.
Hover over a course to read the **course description**, and click to **add a course** to your profile! Click on the **drop button** in your major panel to drop a course.
Your personalized **major panel** on the left will automatically update with which core and elective classes you still need to take.
<img alt="image" src="static/screenshots/major_plan_popup.png" />

<h3>Explore Page<h3>
The scrollable **topic list** in the left panel displays some popular topics in CS, as well as specialized topics (such as Accessibility) that our professors research. Click on each topic to view a **popup** with more information!
<img alt="image" src="static/screenshots/explore_popup.png" />

## Authors
* Nina Howley '27
* Aileen Liang '28

## Quick Start

1. **Clone the repository**
    ```
    git clone https://github.com/ninahowley/cs-hub.git
    ```
2. **Optional: create a [virtual environment](https://gist.github.com/ryumada/c22133988fd1c22a66e4ed1b23eca233).**
3. **Install flask**
    ```
    pip install flask
    ```
4. **Run the app!**

   Mac: ```flask --app app run```

   Windows: ```python app.py```

## Contents

+ ```templates/``` contains html files for all webpages.
    + ```templates/index.html``` contains the main webpage with login and spring '26 courses.
    + ```templates/major-plan.html``` contains a personalized major planning page, including requirements and all Wellesley CS courses.
    + ```templates/explore.html``` contains explore page with topic list and information popups.
+ ```app.py``` is the main app, handling routing with Flask.
+ ```static/``` contains the styling template and formatted .json files for CS course data.
+ ```courses/``` contains scraped CS course data from the Wellesley College courselist.
+ ```db_functions.py``` contains database functions (using SQLite).

## Technology Stack
+ **Frontend:** Flask, HTMl, CSS, JavaScript
+ **Backend:** Python and SQLite

## Our Design Process-- Milestones and Next Steps

**Milestone 1:**
+ Scrape courses (separate core vs elective courses)
+ Create the three pages with navigation bar and basic routing

**Milestone 2:**
+ Implement major tracking page with checklist
+ Implement explore page with clickable topics

**Milestone 3:**
+ Add popups to explore page and course offerings
+ Add information to explore page

**Next Steps:**
+ Add more topics and opportunities to the explore page
+ Allow classes to be added or dropped from the home page spring offerings
+ Allow users to indicate if they skipped courses or took cross-register equivalents
+ Implement more robust login with passwords
