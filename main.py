from data_gatherer.api import fetch_data_engineer_jobs
from transformer.transformer import transform_data
from database.database import export_to_sqlite
from logger.logger import logger

def main():
    try:
        # Log the start of the process
        logger.info('Starting the data collection and export process')

        # Gather Data Engineer job ads using the API
        raw_data = fetch_data_engineer_jobs()
        if not raw_data:
            logger.warning('No data fetched from the API')

        # Transform the data using pandas
        transformed_data = transform_data(raw_data)

        # Export the transformed data to an SQLite database
        export_to_sqlite(transformed_data, 'data_engineer_jobs.db')

        # Log the successful completion of the process
        logger.info('Data collection and export process completed successfully')

    except Exception as e:
        logger.error(f'An error occurred: {e}', exc_info=True)

if __name__ == '__main__':
    main()
