from flask import request, redirect, url_for, render_template
from flask import Flask, request, render_template, redirect, url_for
from neo_DB import unbook_car, order_car, create_customer, update_customer, delete_customer, create_employee, update_employee, delete_employee, Car, UpdateCar, DeleteCar, transition_to_rent

app = Flask(__name__)

# for ease of use, the flask code and components are in a separate file from the Neo4j code. the imports are listed above, the functions are called in their respective flask functions


@app.route('/')  # route for main homepage
def home():
    return render_template('homepage.html')


# main employee route, has three choices of creating, deleting and updating information
@app.route('/employee', methods=['GET', 'POST'])
def employeeRoute():
    if request.method == 'POST':
        action = request.form['action']
        employee_id = request.form.get('employee_id')
        name = request.form.get('name')
        position = request.form.get('position')
        age = request.form.get('age')
        address = request.form.get('address')
        branch = request.form.get('branch')

        if action == 'create':  # simple nav bar to choose the actions we want to do
            create_employee(employee_id, name, position,
                            int(age), address, branch)
        elif action == 'update' and employee_id:
            update_employee(employee_id, name=name, position=position, age=int(
                age) if age else None, address=address, branch=branch)
        elif action == 'delete' and employee_id:
            delete_employee(employee_id)

        return redirect(url_for('success'))

    return render_template('employee_manager.html')


@app.route('/customer', methods=['GET', 'POST'])  # same idea as emloyee route
def customerRoute():
    if request.method == 'POST':
        action = request.form['action']
        name = request.form.get('name')
        address = request.form.get('address')
        branch = request.form.get('branch')
        customerID = request.form.get('customerID')

        if action == 'create':  # same nav bar for employees, we choose what action we want to take
            create_customer(name, address, branch, customerID)
        elif action == 'update' and name and address:
            update_customer(name=name, address=address, branch=branch)
        elif action == 'delete' and name and address:
            delete_customer(name)

        return redirect(url_for('success'))

    return render_template('customer_manager.html')


@app.route('/Car', methods=['GET', 'POST'])  # route for car
def CarRoute():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':  # samen nav bar as the others, but for cars
            # Handle creation of a new car
            car_id = request.form['car_id']
            make = request.form['make']
            model = request.form['model']
            year = int(request.form['year'])
            location = request.form['location']
            status = request.form['status']
            damage = request.form['damage']
            Car(car_id, make, model, year, location, status, damage)
            return redirect(url_for('success'))

        elif action == 'update':
            car_id = request.form['car_id']
            make = request.form['make']
            model = request.form['model']
            year = int(request.form['year'])
            location = request.form['location']
            status = request.form['status']
            damage = request.form['damage']
            UpdateCar(car_id, make, model, year, location, status, damage)
            return redirect(url_for('success'))

        elif action == 'delete':
            car_id = request.form['car_id']
            DeleteCar(car_id)
            return redirect(url_for('success'))

    return render_template('Car.html')


# route for car orders, passes the car id and the customer id
@app.route('/create_order', methods=['GET', 'POST'])
def ordersRoute():
    if request.method == 'POST':
        customerID = request.form.get('customerID')
        car_id = request.form.get('car_id')

        result_message = order_car(customerID, car_id)
        return render_template('order_result.html', message=result_message)

    return render_template('order_manager.html')

# route for renting the booked car


@app.route('/rent_car', methods=['GET', 'POST'])
def rent_car_route():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        car_id = request.form.get('car_id')
        transition_to_rent(customer_id, car_id)
        return redirect(url_for('success'))
    return render_template('rent_car.html')


# route for unbooking or cancelling the car order, passes customer, car id and an update for any damage after renting
@app.route('/unbook_car', methods=['GET', 'POST'])
def unbook_car_route():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        car_id = request.form.get('car_id')
        damage = request.form.get('damage')
        unbook_car(customer_id, car_id, damage)
        return redirect(url_for('success'))
    return render_template('unbook_car.html')


@app.route('/success')  # basic success screen for when a fuction passes
def success():
    return 'Operation completed successfully!'


if __name__ == '__main__':  # main, duh
    app.run(debug=True)
