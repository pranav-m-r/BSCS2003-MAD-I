from flask import Flask, render_template, request
import csv
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        if request.form["ID"] == "student_id":
            try:
                student_id = request.form["id_value"]
                data = []
                with open("data.csv", "r") as f:
                    data = list(csv.reader(f))
                    data.pop(0)
                    data = [i for i in data if i[0] == student_id]
                    total = sum(int(i[2]) for i in data)
                if len(data) == 0:
                    raise ValueError("Student ID not found")
                else:
                    return render_template("student_details.html", data=data, total=total)
            except ValueError:
                return render_template("error.html")
        elif request.form["ID"] == "course_id":
            try:
                course_id = request.form["id_value"]
                marks = []
                with open("data.csv", "r") as f:
                    data = list(csv.reader(f))
                    data.pop(0)
                    marks = [int(i[2]) for i in data if int(i[1]) == int(course_id)]
                if len(marks) == 0:
                    raise ValueError("Course ID not found")
                else:
                    avg = sum(marks) / len(marks)
                    maxi = max(marks)
                    plt.hist(marks)
                    plt.xlabel('Marks')
                    plt.ylabel('Frequency')
                    plt.savefig('static//image.jpg')
                    return render_template("course_details.html", avg=avg, maxi=maxi)
            except ValueError:
                return render_template("error.html")
        else:
            return render_template("error.html")
    else:
        return render_template("error.html")

if __name__ == '__main__':
    app.debug = True
    app.run()