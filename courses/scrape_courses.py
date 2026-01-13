import re
import csv
import pandas as pd

courses = []
core_courses = ["CS 111", "CS 111L", "CS 230", "CS 230L", "CS 231", "CS 235", "CS 240", "CS 240L"]
with open("courses.txt", 'r') as file:
    content = file.read()
    data = re.split(r'\b(?:Available|Unavailable)\b', content)
    for d in data:
        info = d.split("\n")
        try:
            course_tag = info[1].split(" - ")[0]
            course_name = info[2]
            course_instructor = info[3]
            course_distribs_raw = info[1].split("Distribution(s): ")
            if len(course_distribs_raw) == 1:
                course_distribs = None
            else:
                course_distribs = course_distribs_raw[1].split(";")[0]
            course_core = False
            if course_tag in core_courses:
                course_core = True
            courses.append(
                {
                "course_tag": course_tag,
                "course_name": course_name,
                "course_instructor": course_instructor,
                "course_distribs": course_distribs,
                "course_core": course_core
                })
        except Exception as e:
            pass

courses_df = pd.DataFrame(courses)
courses_df = courses_df.drop_duplicates()
courses_df.to_csv('courses.csv', index=False)


