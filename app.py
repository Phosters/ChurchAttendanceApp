from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

members = [
    {'name': 'John Doe', 'number': '12345', 'gender': 'male', 'class': 'Angel'},
    {'name': 'Jane Smith', 'number': '23456', 'gender': 'female', 'class': 'Adults'}
]
attendance = []

classes = ['Angel', 'Matthew', 'New Breed', 'Adults']
genders = ['male', 'female']

home_template = '''
<h2>Attendance Capture</h2>
<form action="/search" method="post">
    Search Name: <input type="text" name="name">
    <input type="submit" value="Search">
</form>
<br>
<form action="/new" method="get">
    <input type="submit" value="Add New Attendance">
</form>
'''

search_result_template = '''
<h2>Search Results for "{{ search_name }}"</h2>
{% if member %}
    <form action="/attend" method="post">
        <input type="hidden" name="name" value="{{ member['name'] }}">
        <input type="hidden" name="class" value="{{ member['class'] }}">
        <input type="hidden" name="gender" value="{{ member['gender'] }}">
        <button type="submit">Mark Present</button>
    </form>
{% else %}
    <p>Not a member. <a href="{{ url_for('new_attendance') }}">Add Details</a></p>
{% endif %}
'''

new_attendance_template = '''
<h2>Add New Attendee</h2>
<form action="/attend" method="post">
    Name: <input type="text" name="name"><br>
    Number: <input type="text" name="number"><br>
    Gender: 
    <select name="gender">
    {% for g in genders %}
        <option value="{{ g }}">{{ g }}</option>
    {% endfor %}
    </select><br>
    Class:
    <select name="class">
    {% for c in classes %}
        <option value="{{ c }}">{{ c }}</option>
    {% endfor %}
    </select><br>
    <button type="submit">Mark Present</button>
</form>
'''

attendance_template = '''
<h2>Attendance Recorded</h2>
<p>{{ name }} was marked present in {{ class_name }} ({{ gender }})</p>
<p><a href="{{ url_for('home') }}">Back to Home</a></p>
'''

@app.route('/')
def home():
    return render_template_string(home_template)

@app.route('/search', methods=['POST'])
def search():
    search_name = request.form['name']
    member = next((m for m in members if m['name'].lower() == search_name.lower()), None)
    return render_template_string(search_result_template, search_name=search_name, member=member)

@app.route('/new')
def new_attendance():
    return render_template_string(new_attendance_template, classes=classes, genders=genders)

@app.route('/attend', methods=['POST'])
def attend():
    name = request.form.get('name')
    number = request.form.get('number', '')
    gender = request.form.get('gender')
    class_name = request.form.get('class')
    if not any(m['name'].lower() == name.lower() for m in members):
        members.append({'name': name, 'number': number, 'gender': gender, 'class': class_name})
    attendance.append({'name': name, 'class': class_name, 'gender': gender})
    return render_template_string(attendance_template, name=name, class_name=class_name, gender=gender)

if __name__ == '__main__':
    app.run(debug=True)
