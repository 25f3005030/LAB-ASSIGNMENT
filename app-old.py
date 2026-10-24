import csv
import sys
import matplotlib.pyplot as plt
import pyhtml as h

student_id_list = []
student_course_marks = 0
total_marks = 0
course_marks_list = []
flag = True

if len(sys.argv) == 3:
  id_argument = sys.argv[1]

  if id_argument == "-c":
    id_type = "course_id"
    id = sys.argv[2].strip()

  elif id_argument == "-s":
    id_type = "student_id"
    id = sys.argv[2].strip()

  else:
    id_type = "invalid"
    id = -1
    flag = False

else:
  flag = False

if flag:
  try:
    with open("data.csv", mode="r", encoding="utf-8") as file:
      reader = csv.reader(file)
      header = next(reader)

      for row in reader:
        student_id = row[0].strip()
        course_id = row[1].strip()
        marks = int(row[2].strip())

        if student_id == id:
          student_id_list.append([student_id, course_id, marks])
          total_marks += marks
        if course_id == id:
          course_marks_list.append(marks)
          student_course_marks += marks

    if (id_type == "student_id" and len(student_id_list) == 0) or (
        id_type == "course_id" and len(course_marks_list) == 0
    ):
      flag = False
  except Exception:
    flag = False

# CSS styling for separated table and cell borders matching the reference image
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

# HTML Generation based on validation flag and input type
if not flag:
  page = h.html(
      h.head(h.title("Something Went Wrong")),
      h.body(h.h1("Wrong Inputs"), h.p("Something went wrong")),
  )
  html_output = "<!DOCTYPE html>\n" + str(page)

elif flag == True and id_type == "student_id":
  page = h.html(
      h.head(h.title("Student Data"), h.style(table_style)),
      h.body(
          h.h1("Student Details"),
          h.table(
              h.tr(h.th("Student id"), h.th("Course id"), h.th("Marks")),
              *[
                  h.tr(h.td(sid), h.td(cid), h.td(m))
                  for sid, cid, m in student_id_list
              ],
              h.tr(h.td("Total Marks"), h.td(""), h.td(total_marks)),
          ),
      ),
  )
  html_output = "<!DOCTYPE html>\n" + str(page)

elif flag == True and id_type == "course_id":
  max_marks = max(course_marks_list)
  avg_marks = sum(course_marks_list) / len(course_marks_list)

  plt.figure()
  plt.hist(course_marks_list)
  plt.xlabel("Marks")
  plt.ylabel("Frequency")
  plt.savefig("image.png")
  plt.close()

  page = h.html(
      h.head(h.title("Course Data"), h.style(table_style)),
      h.body(
          h.h1("Course Details"),
          h.table(
              h.tr(h.th("Average Marks"), h.th("Maximum Marks")),
              h.tr(h.td(avg_marks), h.td(max_marks)),
          ),
          h.img(src="image.png"),
      ),
  )
  html_output = "<!DOCTYPE html>\n" + str(page)

# Write out the final HTML file
with open("output.html", "w", encoding="utf-8") as f:
  f.write(html_output)