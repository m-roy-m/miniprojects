from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# our magical student vault
students = []

# homepage + display + form
@app.route("/")
def home():
    return render_template_string("""
        <h1>🏰 Welcome to Hogwarts High School Student System</h1>

        <form method="POST" action="/add">
            <h3>🧑‍🎓 Add a Student</h3>
            Name: <input name="name"><br>
            Grade: <input name="grade"><br>
            Age: <input name="age"><br>
            <button type="submit">Add</button>
        </form>

        <form method="GET" action="/search">
            <h3>🔍 Search a Student</h3>
            Name: <input name="query"><br>
            <button type="submit">Search</button>
        </form>

        <h2>📜 Current Students</h2>
        <ul>
        {% for i, s in enumerate(students) %}
            <li>
                {{ s.name }} - Grade {{ s.grade }}, Age {{ s.age }}
                [<a href="/delete/{{ i }}">Delete</a>]
                [<a href="/update/{{ i }}">Update</a>]
            </li>
        {% endfor %}
        </ul>
    """, students=students)

# add student
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    grade = request.form["grade"]
    age = request.form["age"]
    students.append({"name": name, "grade": grade, "age": age})
    return redirect("/")

# delete student
@app.route("/delete/<int:index>")
def delete_student(index):
    if 0 <= index < len(students):
        students.pop(index)
    return redirect("/")

# update form
@app.route("/update/<int:index>", methods=["GET", "POST"])
def update_student(index):
    if request.method == "POST":
        students[index]["name"] = request.form["name"]
        students[index]["grade"] = request.form["grade"]
        students[index]["age"] = request.form["age"]
        return redirect("/")
    
    student = students[index]
    return render_template_string("""
        <h2>📝 Update Student</h2>
        <form method="POST">
            Name: <input name="name" value="{{ student.name }}"><br>
            Grade: <input name="grade" value="{{ student.grade }}"><br>
            Age: <input name="age" value="{{ student.age }}"><br>
            <button type="submit">Update</button>
        </form>
        <a href="/">Back</a>
    """, student=student)

# search student by name
@app.route("/search")
def search_student():
    query = request.args.get("query", "").lower()
    results = [s for s in students if query in s["name"].lower()]
    return render_template_string("""
        <h2>🔍 Search Results</h2>
        {% if results %}
            <ul>
            {% for s in results %}
                <li>{{ s.name }} - Grade {{ s.grade }}, Age {{ s.age }}</li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No student found named '{{ query }}'.</p>
        {% endif %}
        <a href="/">Back</a>
    """, results=results, query=query)

# run the thing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
