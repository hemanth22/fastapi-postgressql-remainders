from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
import os

# Define FastAPI app
app = FastAPI()

# Define the request model
class Reminder(BaseModel):
    message_date: str  # Format: DD-MM-YYYY
    message: str

# PostgreSQL connection details
DB_HOST = os.environ.get('postgres_hostname')
DB_NAME = os.environ.get('postgres_database')
DB_PORT = os.environ.get('postgres_port')
DB_USER = os.environ.get('postgres_username')
DB_PASSWORD = os.environ.get('postgres_password')

# Endpoint to accept JSON and insert into PostgreSQL
@app.post("/add_reminder/")
async def add_reminder(reminder: Reminder):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()

        # Insert the reminder into the database
        insert_query = """
            INSERT INTO remainder_messages (message_date, message)
            VALUES (TO_DATE(%s, 'DD-MM-YYYY'), %s)
        """
        cursor.execute(insert_query, (reminder.message_date, reminder.message))

        # Commit the transaction
        connection.commit()
        return {"status": "success", "detail": "Reminder added successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Close the connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
