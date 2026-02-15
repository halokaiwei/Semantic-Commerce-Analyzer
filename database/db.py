import os
import pymysql
from dotenv import load_dotenv

load_dotenv()
def get_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST", "mysql"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "carousell"),
            charset="utf8mb4",
            port=3306,   
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        import logging
        logging.getLogger(__name__).error(f"Failed to connect: {e}")
        raise
