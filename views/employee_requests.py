import sqlite3
import json
from models import Employee

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis",
        "address": "35498 Madison Ave",
        "location_id": 2
    },
    {
        "id": 2,
        "name": "Vienna Brad",
        "address": "35498 Madison Ave",
        "location_id": 2
    }
]

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        """)

        # Initialize an empty list to hold all animal representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'])

            employees.append(employee.__dict__)

    return employees

# Function with a single parameter
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
         SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        employee = Employee(data['id'], data['name'], data['address'])

        return employee.__dict__
    
def create_employee(employee):
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee

def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
     if employee["id"] == id:     
        employee_index = index
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)
def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break

# def get_employee_by_location(location):

#     with sqlite3.connect("./kennel.sqlite3") as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         db_cursor.execute("""
#          SELECT
#             e.id,
#             e.name,
#             e.address,
#             e.location_id
#         FROM employee e
#         WHERE c.id = ?
#         """, ( location, ))

#         employees = []
#         dataset = db_cursor.fetchall()

#         for row in dataset:
#             employee = Employee