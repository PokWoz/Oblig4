from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Adjust this if your Neo4j server URI differs
username = "neo4j"              # Replace with your Neo4j username
password = "password"           # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))


def employee(name, position, age):
    with driver.session() as session:
        query = """
        CREATE (e:Employee {name: $name, position: $position, age: $age})
        RETURN e
        """
        result = session.run(query, name=name, position=position, age=age)
        return result.single()  # Return the created node if needed


def Car(car_id, make, model, year, location, status):
    with driver.session() as session:
        query = """
        CREATE (e:Car {id: $car_id, make: $make, model: $model, year: $year, location: $location, status: $status})
        RETURN e
        """
        result = session.run(query, car_id=car_id, make=make, model=model, year=year, location=location, status=status)
        return result.single()

def UpdateCar(car_id, make, model, year, location, status, damage):
    with driver.session() as session:
        session.run(
            """
            MATCH (c:Car {id: $car_id})
            SET c.make = $make, c.model = $model, c.year = $year, c.location = $location, c.status = $status
            , c.damage=$damage""",
            car_id=car_id, make=make, model=model, year=year, location=location, status=status, damage=damage
        )

def DeleteCar(car_id):
    with driver.session() as session:
        session.run(
            """
            MATCH (c:Car {id: $car_id})
            DELETE c
            """,
            car_id=car_id
        )