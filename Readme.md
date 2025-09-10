# Property Management System
This is a Property Management Database project which aims to handle data related to various aspects of property management, including properties, tenants, leases, maintenance schedules, financial transactions, and property owner information.

This is a Property Management System built using Flask for the backend, Bootstrap for the frontend, and PostgreSQL for the database.

## Database Configuration

This application uses SQLAlchemy for database management, connecting to a PostgreSQL database. The connection details are specified in the `SQLALCHEMY_DATABASE_URI` configuration variable within the application.

## Features

- **User Authentication**: Users can sign up, log in, and manage their properties.
- **Property Listings**: Display a list of available properties with details.
- **Add/Edit/Delete Properties**: Admins can add, edit, and delete property listings.
- **Search and Filter**: Users can search for properties based on location, type, price, etc.
- **Responsive Design**: The frontend is designed using Bootstrap for a seamless experience on different devices.

## Installation

1. Clone this repository:
   ```
   git clone https:https://github.com/Purusharth1/Property-Management.git
   ```

2. Setting Database URI:

   The `SQLALCHEMY_DATABASE_URI` is structured as follows:

   ```
   postgresql://<username>:<password>@<host_name>:<port>/<database_name>
   ```

   - **`<username>`**: The username required to authenticate with the PostgreSQL database.
   - **`<password>`**: The password associated with the database user.
   - **`<host_name>`**: The host name or IP address of the PostgreSQL server.
   - **`<port>`**: The port on which the PostgreSQL server is listening (default is usually `5432`).
   - **`<database_name>`**: The name of the database you want to connect to.

   ### Example Configuration

    Here's an example of how the configuration might look in your `app.py` or `config.py` file:

    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myusername:mypassword@localhost:5432/mydatabase'
    ```


3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your PostgreSQL database:
   - Create a database named `property_db`.

5. Run the application:
   ```
   flask run
   ```

## Contributing

Contributions are welcome! Please create a pull request with your improvements.
