import pymysql
import logging

logger = logging.getLogger(__name__)

def create_crawled_items(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crawled_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_number VARCHAR(255),
            seller_name VARCHAR(255),
            seller_id VARCHAR(255),
            title VARCHAR(255),
            description TEXT,
            category VARCHAR(255),
            price VARCHAR(255),
            images JSON,
            downloaded TINYINT(1) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def create_similar_items(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS similar_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_number1 VARCHAR(255),
            item_number2 VARCHAR(255),
            reason VARCHAR(255),
            details_highest_sim FLOAT DEFAULT NULL,
            images_highest_sim FLOAT DEFAULT NULL,
            is_verified TINYINT(1) DEFAULT 0,
            is_identified TINYINT(1) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uniq_pair (item_number1, item_number2)
        )
    """)

def create_image_similarities(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_similarities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_path1 VARCHAR(255),
            image_path2 VARCHAR(255),
            similarity FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def run_migrations(connection):
    try:
        cursor = connection.cursor()
        logger.info("Running DB migrations...")

        create_crawled_items(cursor)
        create_similar_items(cursor)
        create_image_similarities(cursor)

        connection.commit()
        logger.info("DB migrations completed.")
    except Exception as e:
        logger.exception(f"Migration failed: {e}")
        raise
    finally:
        cursor.close()
