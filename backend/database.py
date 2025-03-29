import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Establish connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def store_ats_result(result):
    """Store ATS result in SQL database"""
    sql = """
    INSERT INTO ats_results (match_percentage, candidate_name, candidate_email, 
                             candidate_phone_number, candidate_year_of_experience)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        result["match_percentage"],
        result["candidate_name"],
        result["candidate_email"],
        result["candidate_phone_number"],
        result["candidate_year_of_experience"]
    )

    cursor.execute(sql, values)
    conn.commit()

    print("✅ ATS result stored in database!")

