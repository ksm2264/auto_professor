import os
import getpass
import random
import string
import subprocess
import toml
import psycopg2

# Create the PostgreSQL data directory if it doesn't exist
data_dir = "postgres_data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Initialize the PostgreSQL data directory
subprocess.run(["initdb", "-D", data_dir])

# Start the PostgreSQL server
subprocess.Popen(["pg_ctl", "-D", data_dir, "start"])

# Generate a random password
password_length = 16
password = ''.join(random.choices(string.ascii_letters + string.digits, k=password_length))

# Set the PostgreSQL user to the system username
username = getpass.getuser()

subprocess.run(["psql", "-U", username, "-d", "postgres", "-c", f"CREATE USER {username} WITH PASSWORD '{password}';"])
subprocess.run(["psql", "-U", username, "-d", "postgres", "-c", f"ALTER USER {username} WITH SUPERUSER;"])

# Create a local folder called 'postgres_config' if it doesn't exist
credentials_dir = "postgres_config"
if not os.path.exists(credentials_dir):
    os.makedirs(credentials_dir)

# Store the PostgreSQL connection information in the 'postgres_config' folder
config = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": username,
    "user": username,
    "password": password
}

with open(os.path.join(credentials_dir, "config.toml"), "w") as f:
    toml.dump(config, f)

print("PostgreSQL server started and credentials saved to 'postgres_config/config.toml'.")


def create_database(database_name: str):
    conn = psycopg2.connect(host="127.0.0.1", port=5432, dbname="postgres", user=username, password=password)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {database_name} WITH OWNER {username};")

    cur.close()
    conn.close()

subprocess.run(["psql", "-U", username, "-d", "postgres", "-c", f"CREATE USER {username} WITH PASSWORD '{password}';"])
subprocess.run(["psql", "-U", username, "-d", "postgres", "-c", f"ALTER USER {username} WITH SUPERUSER;"])

# Create the database
create_database(username)

