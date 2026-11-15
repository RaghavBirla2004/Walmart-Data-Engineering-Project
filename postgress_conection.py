# what this code do- Create Table on Postgres Database using ENV file for Credentials and Load CSV data into Postgres Table 
# CSV File is in /dataset/data/*.csv
# Schema is in /dataset/ddl/walmart_schema.sql

import os
import sys
import psycopg2
from dotenv import load_dotenv

# Ensure utf-8 encoding for standard output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

# PostgreSQL credentials
user = os.getenv("POSTGRES_DB_USER")
password = os.getenv("POSTGRES_DB_PASSWORD")
database = os.getenv("POSTGRES_DB_NAME")
host = os.getenv("POSTGRES_DB_HOST")
port = os.getenv("POSTGRES_DB_PORT")

# Table DDL schemas
TABLE_SCHEMAS = {
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id BIGINT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(255),
            phone VARCHAR(50),
            city VARCHAR(100),
            province VARCHAR(100),
            country VARCHAR(100),
            created_timestamp TIMESTAMP,
            updated_timestamp TIMESTAMP,
            is_active CHAR(1)
        );
    """,
    "stores": """
        CREATE TABLE IF NOT EXISTS stores (
            store_id BIGINT PRIMARY KEY,
            store_name VARCHAR(255),
            city VARCHAR(100),
            province VARCHAR(100),
            country VARCHAR(100),
            created_timestamp TIMESTAMP,
            updated_timestamp TIMESTAMP,
            is_active CHAR(1)
        );
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id BIGINT PRIMARY KEY,
            product_name VARCHAR(255),
            category VARCHAR(100),
            brand VARCHAR(100),
            price NUMERIC(10,2),
            created_timestamp TIMESTAMP,
            updated_timestamp TIMESTAMP,
            is_active CHAR(1)
        );
    """,
    "employees": """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id BIGINT PRIMARY KEY,
            store_id BIGINT,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            email VARCHAR(255),
            job_title VARCHAR(100),
            salary NUMERIC(10,2),
            created_timestamp TIMESTAMP,
            updated_timestamp TIMESTAMP,
            is_active CHAR(1)
        );
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id BIGINT PRIMARY KEY,
            customer_id BIGINT,
            store_id BIGINT,
            order_timestamp TIMESTAMP,
            payment_method VARCHAR(50),
            order_status VARCHAR(50),
            total_amount NUMERIC(12,2),
            created_timestamp TIMESTAMP,
            updated_timestamp TIMESTAMP,
            is_active CHAR(1)
        );
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id BIGINT PRIMARY KEY,
            order_id BIGINT,
            product_id BIGINT,
            quantity INT,
            unit_price NUMERIC(10,2),
            line_amount NUMERIC(12,2),
            created_timestamp TIMESTAMP,
            updated_timestamp TIMESTAMP,
            is_active CHAR(1)
        );
    """
}

# Tables mapped to their CSV file paths and column list
TABLES_DATA = [
    {
        "table": "customers",
        "file_path": r"dataset/data/customers.csv",
        "columns": "(customer_id, first_name, last_name, email, phone, city, province, country, created_timestamp, updated_timestamp, is_active)"
    },
    {
        "table": "stores",
        "file_path": r"dataset/data/stores.csv",
        "columns": "(store_id, store_name, city, province, country, created_timestamp, updated_timestamp, is_active)"
    },
    {
        "table": "products",
        "file_path": r"dataset/data/products.csv",
        "columns": "(product_id, product_name, category, brand, price, created_timestamp, updated_timestamp, is_active)"
    },
    {
        "table": "employees",
        "file_path": r"dataset/data/employees.csv",
        "columns": "(employee_id, store_id, first_name, last_name, email, job_title, salary, created_timestamp, updated_timestamp, is_active)"
    },
    {
        "table": "orders",
        "file_path": r"dataset/data/orders.csv",
        "columns": "(order_id, customer_id, store_id, order_timestamp, payment_method, order_status, total_amount, created_timestamp, updated_timestamp, is_active)"
    },
    {
        "table": "order_items",
        "file_path": r"dataset/data/order_items.csv",
        "columns": "(order_item_id, order_id, product_id, quantity, unit_price, line_amount, created_timestamp, updated_timestamp, is_active)"
    }
]


def load_all_csv_to_postgres():
    conn = None
    try:
        # Establish connection
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        print("[+] PostgreSQL connection successful!\n")

        # Step 1: Create Tables
        print("--- Step 1: Creating Tables (if not exist) ---")
        for table_name, ddl in TABLE_SCHEMAS.items():
            cursor.execute(ddl)
            print(f"  [+] Table '{table_name}' verified/created.")
        conn.commit()
        print("All tables created successfully.\n")

        # Step 2: Import CSV Data
        print("--- Step 2: Inserting CSV Data ---")
        for item in TABLES_DATA:
            table_name = item["table"]
            file_path = item["file_path"]
            columns = item["columns"]

            if not os.path.exists(file_path):
                print(f"  [-] File not found: {file_path}")
                continue

            # Check existing row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"  [*] Table '{table_name}' already contains {count} records. Skipping to avoid duplicate key errors.")
            else:
                print(f"  [...] Loading '{file_path}' into '{table_name}'...")
                with open(file_path, "r", encoding="utf-8") as file:
                    copy_sql = f"""
                        COPY {table_name} {columns}
                        FROM STDIN
                        WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')
                    """
                    cursor.copy_expert(copy_sql, file)
                conn.commit()

                # Fetch new row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                new_count = cursor.fetchone()[0]
                print(f"  [+] Successfully loaded {new_count} rows into '{table_name}'.")

        # Step 3: Summary of all tables
        print("\n--- Summary of Record Counts in PostgreSQL ---")
        for item in TABLES_DATA:
            table_name = item["table"]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            total = cursor.fetchone()[0]
            print(f"  -> {table_name}: {total} rows")

        cursor.close()
        conn.close()
        print("\n[+] All CSV files imported into PostgreSQL successfully!")

    except psycopg2.Error as e:
        print("\n[-] PostgreSQL operation failed!")
        print("Error:", e)
        if conn:
            conn.rollback()
            conn.close()


if __name__ == "__main__":
    load_all_csv_to_postgres()
