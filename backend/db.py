import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(
            host = 'localhost',
            database = "Task-Manager",
            user = "postgres",
            password = "lifeisgood",
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print(f"Database connection was succesful")
        break
    except Exception as e:
        print(" Connecting to database failed")
        print("Error:", e)
        time.sleep(2)

    