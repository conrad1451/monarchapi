# --- app.py ---
# CHQ: Gemini AI scaffolded this

import os
import json
from flask import Flask, jsonify
import psycopg2
from psycopg2 import sql
from flask_cors import CORS # Import Flask-CORS

# --- Configure Flask Application ---
app = Flask(__name__)
# Enable CORS for all routes and origins to allow the React app to connect
CORS(app) 

# Use the Google VM variable as the user's script does
GOOGLE_VM_DOCKER_HOSTED_SQL = os.getenv('GOOGLE_VM_DOCKER_HOSTED_SQL', '5432')

# --- API Endpoint for Monarch Butterfly Data ---
@app.route('/api/monarchs', methods=['GET'])
def get_monarch_data():
    """
    Fetches all Monarch butterfly occurrence data from the PostgreSQL database
    and returns it as a JSON array.

    The table name is hardcoded for this example based on the user's script.
    You can modify this to accept a query parameter for a dynamic table name.
    """
    # Use a specific table name from the ETL script's output for a concrete example
    table_name = "june212025"
    conn = None
    data = []

    try:
        conn_string_gcp_docker = GOOGLE_VM_DOCKER_HOSTED_SQL

        # conn_string = conn_string_neon
        conn_string = conn_string_gcp_docker

        # Connect to the PostgreSQL database
        # NOTE: The provided script also uses GOOGLE_VM_DOCKER_HOSTED_SQL.
        # This implementation assumes the NEON variables are a standard connection string.
        # If your GOOGLE_VM_DOCKER_HOSTED_SQL is the full connection string, you would use that.
        # Here we'll use the Neon variables as they are more standard for a connection.
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        # Build the query dynamically using psycopg2's sql module to prevent SQL injection
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        
        # Execute the query
        cursor.execute(query)
        
        # Get column names from the cursor description
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch all results and format them into a list of dictionaries
        records = cursor.fetchall()
        for record in records:
            # zip the columns and record values together to create a dictionary
            data.append(dict(zip(columns, record)))

        # Return the data as a JSON response
        return jsonify(data)

    except psycopg2.OperationalError as e:
        # Handle database connection errors gracefully
        print(f"Database connection failed: {e}")
        return jsonify({"error": "Failed to connect to the database."}), 500
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
    finally:
        # Ensure the connection is closed even if an error occurs
        if conn is not None:
            conn.close()

# --- Main Entry Point ---
if __name__ == '__main__':
    # Run the server on a public host and a specified port for containerized environments
    # or for local testing.
    # The 'debug=True' flag is great for development as it provides live reloading.
    app.run(host='0.0.0.0', port=5000, debug=True)
