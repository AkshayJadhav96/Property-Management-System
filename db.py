import psycopg2
from psycopg2 import pool, sql, extras
from flask import session
import os
from dotenv import load_dotenv

# Load database credentials from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")         # default user (e.g., postgres)
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_POOL_MIN_CONN = int(os.getenv("DB_POOL_MIN_CONNECTION", 1))
DB_POOL_MAX_CONN = int(os.getenv("DB_POOL_MAX_CONNECTION", 10))

# Define allowed roles (PostgreSQL roles must match these)
ALLOWED_ROLES = ['tenant', 'owner', 'agent', 'admin']

# Global connection pool
connection_pool = None

# --------------------------------------
# 1. Initialize Threaded Connection Pool
# --------------------------------------
def initialize_connection_pool():
    global connection_pool
    try:
        connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=DB_POOL_MIN_CONN,
            maxconn=DB_POOL_MAX_CONN,
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        # Quick test
        test_conn = connection_pool.getconn()
        with test_conn.cursor() as cur:
            cur.execute("SELECT 1;")
        cur.close()
        # Return the connection back to the pool
        connection_pool.putconn(test_conn)
        print("✅ DB pool initialized")
        return True
    except Exception as e:
        print(f"❌ Failed to init DB pool: {e}")
        return False

# ----------------------------
# 2. Get and Release a Connection
# ----------------------------
def get_db_connection():
    if connection_pool is None:
        initialize_connection_pool()
    return connection_pool.getconn()

def release_db_connection(conn):
    if connection_pool and conn:
        connection_pool.putconn(conn)

# ------------------------------------------------------
# 3. Return role-based connection (uses SET ROLE)
# ------------------------------------------------------
def get_role_based_connection(role: str):
    conn = get_db_connection()
    try:
        if role in ALLOWED_ROLES:
            conn.autocommit = True  # required before SET ROLE
            with conn.cursor() as cur:
                cur.execute(f"SET ROLE {role};")
                # print(f"✅ Set role to {role} for connection")
                # print("Current DB role:", cur.fetchone())
            conn.autocommit = False  # back to normal for transactions
        return conn
    except Exception as e:
        print(f"⚠️ Failed to set role: {e}")
        return conn  # fallback to default if role fails

# ---------------------------------------------------
# 4. Select connection based on session['role'] value
# ---------------------------------------------------
def get_connection_for_request():
    role = session.get("role")  # stored after login
    if role:
        return get_role_based_connection(role)
    return get_db_connection()  # no role (e.g., during login)

# ------------------------------------
# 5. Execute a query (SELECT / INSERT)
# ------------------------------------
def execute_query(query, params=None, fetch=True):
    conn = None
    try:
        conn = get_connection_for_request()
        conn.autocommit = False
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, params)
            result = cur.fetchall() if fetch else None
            conn.commit()
            return result if fetch else True
    except Exception as e:
        print(f"💥 Query error: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            release_db_connection(conn)

# --------------------------
# 6. Optional DB Health Check
# --------------------------
def check_db_connection():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()
        release_db_connection(conn)
        return True
    except Exception as e:
        print(f"❌ DB health check failed: {e}")
        return False
