import pandas as pd
from logger.logger import logger

def transform_data(data):
    try:
        logger.info('Transforming the data into a pandas DataFrame')

        # Extract relevant fields and create a DataFrame
        job_list = []
        for job in data:
            job_list.append({
                'title': job.get('headline'),
                'company': job.get('employer', {}).get('name'),
                'location': job.get('workplace_address', {}).get('municipality'),
                'application deadline': job.get('application_deadline'),
                'webpage': job.get('webpage_url'),
                'description': job.get('description', {}).get('text')
                
            })

        # Convert to a pandas DataFrame
        df = pd.DataFrame(job_list)

        # Clean the data (strip whitespace and remove time from deadline)
        df['title'] = df['title'].str.strip()
        df['company'] = df['company'].str.strip()
        df['location'] = df['location'].str.strip()
        df['application deadline'] = df['application deadline'].str.split('T').str[0].str.strip()
        df['webpage'] = df['webpage'].str.strip()
        df['description'] = df['description'].str.strip()

        logger.info('Data transformation complete')
        return df

    except Exception as e:
        logger.error(f'Error during data transformation: {e}', exc_info=True)
        return pd.DataFrame()  # Return an empty DataFrame in case of error
