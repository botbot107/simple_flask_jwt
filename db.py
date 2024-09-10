import mysql.connector
from config.config import config

def get_db_connection():
    conn = mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USERNAME,
        password=config.DB_PASSWORD
    )
    return conn

def execute_sql_script(script):
    conn = get_db_connection()
    cursor = conn.cursor()
    for statement in script.split(';'):
        if statement.strip():
            cursor.execute(statement)
    conn.commit()
    conn.close()

def run_db_schema_updates():
    # Define SQL scripts to drop and recreate tables
    drop_tables_script = """
    DROP TABLE IF EXISTS click_log;
    DROP TABLE IF EXISTS clients;
    """

    create_tables_script = """
    CREATE TABLE clients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE click_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL,
        click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    insert_dummy_data_script = """
    INSERT INTO clients (user_name, password) 
    VALUES 
    ('john_doe', 'AassrC123@#'), 
    ('jane_doe', 'pAwo#4!rd456');
    """

    # Execute SQL scripts
    execute_sql_script(drop_tables_script)
    execute_sql_script(create_tables_script)
    execute_sql_script(insert_dummy_data_script)

def log_click(user_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO click_log (user_name) VALUES (%s)", (user_name,))
    conn.commit()
    conn.close()

def get_user_by_username(user_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_name, password FROM clients WHERE user_name=%s", (user_name,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_clients_from_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return clients