import csv
import sys
from jinja2 import Template
import matplotlib.pyplot as plt
from collections import Counter

def main():
    try:
      if sys.argv[1] == "-s":
          student_id = sys.argv[2].strip()
          data = []
          with open("data.csv", "r") as f:
              data = list(csv.reader(f))
              data.pop(0)
              data = [i for i in data if i[0] == student_id]
              total = sum(int(i[2]) for i in data)
          if len(data) == 0:
              raise ValueError("Student ID not found")
          t = """
  <!DOCTYPE html>
  <html>
    <head>
      <title>
        Student Data
      </title>
    </head>
    <body>
      <h1>
        Student Details
      </h1>
      <table>
        <tr>
          <th>
            Student ID
          </th>
          <th>
            Course ID
          </th>
          <th>
            Marks
          </th>
        </tr>
        {% for i in data %}
        <tr> 
          <td>{{i[0]}}</td>
          <td>{{i[1]}}</td>
          <td>{{i[2]}}</td>
        </tr>
        {% endfor %}
        <tr>
          <td colspan="2">Total Marks</td>
          <td>{{total}}</td>
        </tr>
      </table>
    </body>
  </html>
  """
          with open("output.html", "w") as f:
              f.write(Template(t).render(data=data, total=total))
              
      elif sys.argv[1] == "-c":
          course_id = sys.argv[2].strip()
          marks = []
          with open("data.csv", "r") as f:
              data = list(csv.reader(f))
              data.pop(0)
              marks = [int(i[2]) for i in data if int(i[1]) == int(course_id)]
          if len(marks) == 0:
              raise ValueError("Course ID not found")
          avg = sum(marks) / len(marks)
          maxi = max(marks)
          t = """
  <!DOCTYPE html>
  <html>
    <head>
      <title>
        Course Data
      </title>
    </head>
    <body>
      <h1>
        Course Details
      </h1>
      <table>
        <tr>
          <th>
            Average Marks
          </th>
          <th>
            Maximum Marks
          </th>
        </tr> 
        <tr>
          <td>{{avg}}</td>
          <td>{{maxi}}</td>
        </tr>
      </table>
      <br>
      <img src="image.jpg">
    </body>
  </html>
  """
          plt.hist(marks)
          plt.xlabel('Marks')
          plt.ylabel('Frequency')
          plt.savefig('image.jpg')
          with open("output.html", "w") as f:
              f.write(Template(t).render(avg=avg, maxi=maxi))
    except ValueError:
        t = """
  <!DOCTYPE html>
  <html>
    <head>
      <title>
        Something Went Wrong
      </title>
    </head>
    <body>
      <h1>
        Wrong Inputs
      </h1>
      <p>
        Something went wrong
      </p>
    </body>
  </html>
  """
        with open("output.html", "w") as f:
              f.write(Template(t).render())

if __name__ == "__main__":
    main()