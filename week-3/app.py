import csv
import sys
import matplotlib.pyplot as plt

# Initialize variables
student_id_list = []
total_marks = 0
course_marks_list = []
flag = True
id_type = ""
id_val = ""

# Parse command line arguments
if len(sys.argv) == 3:
    id_argument = sys.argv[1]
    if id_argument == "-c":
        id_type = "course_id"
        id_val = sys.argv[2].strip()
    elif id_argument == "-s":
        id_type = "student_id"
        id_val = sys.argv[2].strip()
    else:
        flag = False
else:
    flag = False

# Read CSV and filter data
if flag:
    try:
        with open("data.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            
            for row in reader:
                if len(row) < 3:
                    continue
                student_id = row[0].strip()
                course_id = row[1].strip()
                try:
                    marks = int(row[2].strip())
                except ValueError:
                    continue

                if id_type == "student_id" and student_id == id_val:
                    student_id_list.append([student_id, course_id, marks])
                    total_marks += marks
                elif id_type == "course_id" and course_id == id_val:
                    course_marks_list.append(marks)

        # Check if ID matched anything in the CSV
        if (id_type == "student_id" and len(student_id_list) == 0) or \
           (id_type == "course_id" and len(course_marks_list) == 0):
            flag = False
    except Exception:
        flag = False

# CSS styling for tables matching reference formatting
table_style = """
    table {
        border: 1px solid black;
        border-collapse: separate;
        border-spacing: 2px;
    }
    th, td {
        border: 1px solid black;
        padding: 5px;
    }
"""

# Generate HTML output based on state
if not flag:
    html_output = f"""<!DOCTYPE html>
<html>
<head>
    <title>Something Went Wrong</title>
</head>
<body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
</body>
</html>"""

elif id_type == "student_id":
    rows_html = ""
    for sid, cid, m in student_id_list:
        rows_html += f"        <tr><td>{sid}</td><td>{cid}</td><td>{m}</td></tr>\n"
    
    html_output = f"""<!DOCTYPE html>
<html>
<head>
    <title>Student Data</title>
    <style>{table_style}</style>
</head>
<body>
    <h1>Student Details</h1>
    <table>
        <tr><th>Student ID</th><th>Course ID</th><th>Marks</th></tr>
{rows_html}        <tr><td>Total Marks</td><td></td><td>{total_marks}</td></tr>
    </table>
</body>
</html>"""

elif id_type == "course_id":
    max_marks = max(course_marks_list)
    avg_marks = sum(course_marks_list) / len(course_marks_list)

    # Generate and save histogram
    plt.figure()
    plt.hist(course_marks_list)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig("image.png")
    plt.close()

    html_output = f"""<!DOCTYPE html>
<html>
<head>
    <title>Course Data</title>
    <style>{table_style}</style>
</head>
<body>
    <h1>Course Details</h1>
    <table>
        <tr><th>Average Marks</th><th>Maximum Marks</th></tr>
        <tr><td>{avg_marks}</td><td>{max_marks}</td></tr>
    </table>
    <img src="image.png" alt="Marks Histogram">
</body>
</html>"""

# Write out the final HTML file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_output)