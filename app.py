from flask import Flask, request, render_template, redirect, url_for
import os
from neo_DB import employee, Car, UpdateCar, DeleteCar

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route('/employee', methods=['GET', 'POST'])
def employeeRoute():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        age = int(request.form['age'])
        address = request.form["address"]
        branch = request.form["branch"]
        employee(name, position, age, address, branch)
        return redirect(url_for('success'))

    return render_template('employee_manager.html')



from flask import request, redirect, url_for, render_template

@app.route('/Car', methods=['GET', 'POST'])
def CarRoute():
    if request.method == 'POST':
        action = request.form.get('action')  # Get selected action from form
        
        if action == 'create':
            # Handle creation of a new car
            car_id = request.form['car_id']
            make = request.form['make']
            model = request.form['model']
            year = int(request.form['year'])
            location = request.form['location']
            status = request.form['status']
            damage = request.form["damage"]
            Car(car_id, make, model, year, location, status)  # Assuming `Car` is a function or class for handling car creation
            return redirect(url_for('success'))

        elif action == 'update':
            car_id = request.form['car_id'] 
            make = request.form['make']
            model = request.form['model']
            year = int(request.form['year'])
            location = request.form['location']
            status = request.form['status']
            damage = request.form["damage"]
            UpdateCar(car_id, make, model, year, location, status, damage)  # Define `update_car` for updating in Neo4j
            return redirect(url_for('success'))

        elif action == 'delete':
            # Handle deletion of a car
            car_id = request.form['car_id']  # Example: ID of car to delete
            DeleteCar(car_id)  # Define `delete_car` for deletion in Neo4j
            return redirect(url_for('success'))

    return render_template('Car.html')  # Render initial form



@app.route('/success')
def success():
    return "Operation completed successfully!"

if __name__ == '__main__':
    app.run(debug=True)
