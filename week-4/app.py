from flask import Flask,url_for,render_template,request 
import csv 
import os 
import matplotlib
matplotlib.use('Agg') # GUI window error से बचने के लिए
import matplotlib.pyplot as plt

app=Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        id_type=request.form.get('ID')
        id_value=request.form.get('id_value')

        if not id_type or not id_value:
            return render_template('error.html')

        
        if id_type=='student_id':
            records=[]
            total_marks=0

            if os.path.exists('data.csv'):
                with open('data.csv', mode='r') as file:
                    reader = csv.reader(file)
                    next(reader) # Header row को skip करने के लिए
                    for row in reader:
                        if len(row) >= 3:
                            csv_student_id = row[0].strip()
                            if csv_student_id == str(id_value).strip():
                                # Dictionary format में डेटा बनाएं ताकि HTML template में आसानी से दिखे
                                record = {
                                    'Student id': row[0].strip(),
                                    'Course id': row[1].strip(),
                                    'Marks': row[2].strip()
                                }
                                records.append(record)
                                total_marks += float(row[2].strip())

            if not records:
                
                return render_template('error.html')
                
            return render_template('student_details.html', records=records, total_marks=total_marks)
    
        elif id_type=='course_id':
            marks_list = []

            if os.path.exists('data.csv'):
                            with open('data.csv', mode='r') as file:
                                reader = csv.reader(file)
                                next(reader) # Header row को skip करने के लिए
                                for row in reader:
                                    if len(row) >= 3:
                                         if row[1].strip() == id_value:
                                            marks_list.append(float(row[2].strip()))
    
            if not marks_list:
                
                return render_template('error.html')

            avg_marks = round(sum(marks_list) / len(marks_list), 2)
            max_marks = max(marks_list)

            plt.figure(figsize=(6, 4))
            # bins='auto' करने से Matplotlib डेटा के अनुसार सही कॉलम खुद बना लेगा
            plt.hist(marks_list, bins='auto', edgecolor='black', color='skyblue')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            plt.title('Marks Distribution')
            plt.tight_layout()

            plot_path = os.path.join('static', 'plot.png')
            plt.savefig(plot_path)
            plt.close()

            return render_template('course_details.html', avg_marks=avg_marks, max_marks=max_marks)

        

    return render_template('home.html',id_type='student_id')




if __name__ == '__main__':
    app.run(debug=True)

