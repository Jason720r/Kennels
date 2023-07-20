import sqlite3
import json
from models import Customer


CUSTOMERS = [
    {
        "id": 1,
        "name": "Ryan Tanay",
        "address": "201 Created St",
        "email": "mo@silvera.com",
        "password": "password"
    },
     {
        "id": 2,
        "name": "Tom Riddle",
        "address": "201 Created St",
        "email": "mo@silvera.com",
        "password": "password"
    }
]

def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        """)

        # Initialize an empty list to hold all animal representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'],
                                row['email'], row['password'])

            customers.append(customer.__dict__)

    return customers

# Function with a single parameter
def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
         SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        customer = Customer(data['id'], data['name'], data['address'],
                            data['email'], data['password'])

        return customer.__dict__

def create_customer(customer):
    # Get the id value of the last employee in the list
    max_id = CUSTOMERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    customer["id"] = new_id

    # Add the employee dictionary to the list
    CUSTOMERS.append(customer)

    # Return the dictionary with `id` property added
    return customer
def delete_customer(id):
    customer_index = -1
    for index, customer in enumerate(CUSTOMERS):
     if customer["id"] == id:     
        customer_index = index
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)
def update_customer(id, new_customer):
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            CUSTOMERS[index] = new_customer
            break

def get_customers_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return customers