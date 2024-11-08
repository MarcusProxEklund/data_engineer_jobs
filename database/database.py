import sqlite3
from logger.logger import logger

def export_to_sqlite(df, db_filename):
    try:
        logger.info(f'Exporting data to SQLite database: {db_filename}')

        # Connect to SQLite database
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_engineer_jobs (
                id INTEGER PRIMARY KEY,
                title TEXT,
                company TEXT,
                location TEXT,
                application_deadline TEXT,
                webpage TEXT,
                description TEXT
            )
        ''')

        # Insert data into the table
        df.to_sql('data_engineer_jobs', conn, if_exists='replace', index=False)
        
        # Commit and close the connection
        conn.commit()
        conn.close()

        logger.info('Data successfully exported to SQLite database')

    except Exception as e:
        logger.error(f'Error exporting data to SQLite database: {e}', exc_info=True)
