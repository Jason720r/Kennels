CUSTOMERS = [
    {
        "id": 1,
        "name": "Ryan Tanay"
    },
     {
        "id": 2,
        "name": "Tom Riddle"
    }
]

def get_all_customers():
    return CUSTOMERS

# Function with a single parameter
def get_single_customer(id):
    # Variable to hold the found animal, if it exists
    requested_customer = None

    # Iterate the requested_customers list above. Very similar to the
    # for..of loops you used in JavaScript.
    for customer in CUSTOMERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer

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