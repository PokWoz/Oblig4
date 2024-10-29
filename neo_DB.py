from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # Adjust this if your Neo4j server URI differs
username = "neo4j"              # Replace with your Neo4j username
password = "password"           # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))


def create_employee(name, position, age):
    with driver.session() as session:
        query = """
        CREATE (e:Employee {name: $name, position: $position, age: $age})
        RETURN e
        """
        result = session.run(query, name=name, position=position, age=age)
        return result.single()  # Return the created node if needed
