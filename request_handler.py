import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import get_all_animals, get_single_animal, get_animal_by_location, get_single_location, get_all_locations, get_all_employees, get_single_employee, get_all_customers,get_single_customer, get_customers_by_email, create_animal, create_location, create_employee, create_customer, delete_animal, delete_location, delete_employee, delete_customer, update_animal, update_customer, update_employee, update_location



# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        parsed = self.parse_url(self.path)

        resource = None

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

        if resource == "animals":
            if id is not None:
                response = get_single_animal(id)

            else:
                response = get_all_animals()

        if resource == "locations":
            if id is not None:
                response = get_single_location(id)

            else:
                response = get_all_locations()

        if resource == "employees":
            if id is not None:
                response = get_single_employee(id)

            else:
                response = get_all_employees()

        elif resource == "customers":
            if id is not None:
                response = get_single_customer(id)

            else:
                response = get_all_customers()
        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query is not None and query.get('email') and resource == 'customers':
                response = get_customers_by_email(query['email'][0])
            if query is not None and  query.get('location_id') and resource == 'animals':
                response = get_animal_by_location(query['location_id'][0])
        
            

        self.wfile.write(json.dumps(response).encode())
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)

        # Your new console.log() that outputs to the terminal
        print(self.path)

        # It's an if..else statement
        if self.path == "/animals":
            response = get_all_animals()
        else:
            response = []

        if self.path == "/locations":
            response = get_all_locations()
        else:
            response = []

        if self.path == "/employees":
            response = get_all_employees()
        else:
            response = []

        if self.path == "/customers":
            response = get_all_customers()
        else:
            response = []

        # Send a JSON formatted string as a response
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_location = None
        new_employee = None
        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)
            self.wfile.write(json.dumps(new_animal).encode())
        if resource == "locations":
            new_location = create_location(post_body)
            self.wfile.write(json.dumps(new_location).encode())
        if resource == "employees":
            new_employee = create_employee(post_body)
            self.wfile.write(json.dumps(new_employee).encode())
        if resource == "customers":
            new_customer = create_customer(post_body)
            self.wfile.write(json.dumps(new_customer).encode())
    # A method that handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

    # Delete a single animal from the list
        if resource == "animals":
            success = update_animal(id, post_body)
            self.wfile.write("".encode())
        if resource == "locations":
            update_location(id, post_body)
            self.wfile.write("".encode())
        if resource == "customer":
            update_customer(id, post_body)
            self.wfile.write("".encode())
        if resource == "employees":
            update_employee(id, post_body)
            self.wfile.write("".encode())
            self.do_PUT()

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        
        self.wfile.write("".encode())
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
            # Encode the new animal and send in response
            self.wfile.write("".encode())
        if resource == "locations":
            delete_location(id)
            self.wfile.write("".encode())
        if resource == "employees":
            delete_employee(id)
            self.wfile.write("".encode())
        if resource == "customers":
            delete_customer(id)
            self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
