from flask import Flask, request, render_template, redirect, url_for
import os
from neo_DB import create_employee

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        age = int(request.form['age'])
        create_employee(name, position, age)
        # Redirect to a success page or another endpoint
        return redirect(url_for('success'))

    return render_template('add_employee.html')


@app.route('/success')
def success():
    return "Employee created successfully!"


if __name__ == '__main__':
    app.run(debug=True)
