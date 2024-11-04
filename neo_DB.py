from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Adjust this if your Neo4j server URI differs
username = "neo4j"              # Replace with your Neo4j username
password = "12345678"           # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

# -----------------------------------------------------------------------------------------


# Creates the needed properties for employee node
def create_employee(employee_id, name, position, age, address, branch):
    with driver.session() as session:
        query = """
        CREATE (e:Employee {employee_id: $employee_id, name: $name, position: $position, age: $age, address: $address, branch: $branch})
        RETURN e
        """
        session.run(query, employee_id=employee_id, name=name, position=position,
                    age=age, address=address, branch=branch)


# Gives update function to employee nodes for all properties
def update_employee(employee_id, name=None, position=None, age=None, address=None, branch=None):
    with driver.session() as session:
        query = """
        MATCH (e:Employee {employee_id: $employee_id})
        SET e.name = COALESCE($name, e.name),
            e.position = COALESCE($position, e.position),
            e.age = COALESCE($age, e.age),
            e.address = COALESCE($address, e.address),
            e.branch = COALESCE($branch, e.branch)
        RETURN e
        """
        result = session.run(query, employee_id=employee_id, name=name, position=position,
                             age=age, address=address, branch=branch)
        return result.single()


def delete_employee(employee_id):  # delete employee nodes based on employee ID
    with driver.session() as session:
        query = """
        MATCH (e:Employee {employee_id: $employee_id})
        DETACH DELETE e
        """
        session.run(query, employee_id=employee_id)

# -----------------------------------------------------------------------------------------------


# creates customer nodes with needed properties
def create_customer(name, address, branch, customerID):
    with driver.session() as session:
        query = """
        CREATE (e:Customer {name: $name, address: $address, branch: $branch, customerID: $customerID})
        RETURN e
        """
        session.run(query, name=name,
                    address=address, branch=branch, customerID=customerID)


# functionality to update customer properties
def update_customer(name, address=None, branch=None, customerID=None):
    with driver.session() as session:
        query = """
        # MATCH (e:Customer {customerID: $customerID})
        SET e.name = COALESCE($name, e.name),
            e.address = COALESCE($address, e.address),
            e.branch = COALESCE($branch, e.branch)
        RETURN e
        """
        result = session.run(query,
                             name=name, address=address, branch=branch, customerID=customerID)
        return result.single()


def delete_customer(customerID):  # delete customer by ID
    with driver.session() as session:
        query = """
        MATCH (e:Customer {customerID: $customerID})
        DETACH DELETE e
        """
        session.run(query, customerID=customerID)

# --------------------------------------------------------------------------------------------------------------------------


def order_car(customer_id, car_id):
    with driver.session() as session:
        # Check if the car is available
        availability_query = """
            MATCH (car:Car {car_id: $car_id})
            RETURN car.status AS status
        """
        available_car = session.run(availability_query, car_id=car_id)
        car_status_record = available_car.single()  # Get the first record

        if car_status_record is None:  # Check if no car was found
            return "The car does not exist."

        if car_status_record['status'] == 'Booked':
            return "The car is not available for booking."

        # If the car is available, we change the status to booked now
        update_status_query = """
            MATCH (car:Car {car_id: $car_id})
            SET car.status = 'Booked'
            RETURN car
        """
        session.run(update_status_query, car_id=car_id)

        # we create a relation between the customer and the car that they booked
        order_query = """
            MATCH (c:Customer {customerID: $customer_id}), (car:Car {car_id: $car_id})
            CREATE (c)-[:BOOKED]->(car)
            RETURN c, car
        """
        result = session.run(
            order_query, customer_id=customer_id, car_id=car_id)

        if result.single():
            return "Order created successfully."
        else:
            return "Failed to create order."


def transition_to_rent(customer_id, car_id):
    with driver.session() as session:

        # Step 1: Delete the BOOKED relationship
        delete_booked_relationship_query = """
            MATCH (c:Customer {customerID: $customer_id})-[r:BOOKED]->(car:Car {car_id: $car_id})
            DELETE r
        """
        session.run(delete_booked_relationship_query,
                    customer_id=customer_id, car_id=car_id)

        # Step 2: Create the RENTS relationship between the customer and car
        create_rents_relationship_query = """
            MATCH (c:Customer {customerID: $customer_id}), (car:Car {car_id: $car_id})
            CREATE (c)-[:RENTS]->(car)
        """
        session.run(create_rents_relationship_query,
                    customer_id=customer_id, car_id=car_id)

        update_status_query = """
            MATCH (car:Car {car_id: $car_id})
            SET car.status = 'Rented'
        """
        session.run(update_status_query, car_id=car_id)

        return "Car rented successfully, status updated to rented, and relationship set to RENTS."


def unbook_car(customer_id, car_id, damage):
    with driver.session() as session:
        # Check if the car is currently booked by the specified customer
        check_booking_query = """
            MATCH (c:Customer {customerID: $customer_id})-[r:RENTS]->(car:Car {car_id: $car_id})
            RETURN car.status AS status
        """
        result = session.run(check_booking_query,
                             customer_id=customer_id, car_id=car_id)
        car_status_record = result.single()

        if car_status_record is None or car_status_record['status'] != 'Rented':
            return "The car is not currently rented by this customer."

        delete_relationship_query = """
            MATCH (c:Customer {customerID: $customer_id})-[r:RENTS]->(car:Car {car_id: $car_id})
            DELETE r
        """
        session.run(delete_relationship_query,
                    customer_id=customer_id, car_id=car_id)

        update_damage_query = """
            MATCH (car:Car {car_id: $car_id})
            SET car.damage = $damage
        """
        session.run(update_damage_query, car_id=car_id, damage=damage)

        update_status_query = """
            MATCH (car:Car {car_id: $car_id})
            SET car.status = 'Available'
        """
        session.run(update_status_query, car_id=car_id)

        return "Car unbooked successfully and updated."


# -----------------------------------------------------------------------------------------------


def Car(car_id, make, model, year, location, status, damage):  # Create car with required properties
    with driver.session() as session:
        query = """
        CREATE (e:Car {car_id: $car_id, make: $make, model: $model, year: $year, location: $location, status: $status, damage: $damage})
        RETURN e
        """
        result = session.run(query, car_id=car_id, make=make,
                             model=model, year=year, location=location, status=status, damage=damage)
        return result.single()


def UpdateCar(car_id, make, model, year, location, status, damage):  # update car properties
    with driver.session() as session:
        session.run(
            """
            MATCH (c:Car {id: $car_id})
            SET c.make = $make, c.model = $model, c.year = $year, c.location = $location, c.status = $status
            , c.damage=$damage""",
            car_id=car_id, make=make, model=model, year=year, location=location, status=status, damage=damage
        )


def DeleteCar(car_id):  # delete car by ID
    with driver.session() as session:
        query = (
            """
            MATCH (c:Car {id: $car_id})
            DETACH DELETE c
            """
        )
        session.run(query, car_id=car_id)
