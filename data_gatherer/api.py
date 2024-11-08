import requests
from logger.logger import logger

def fetch_data_engineer_jobs():
    # Base URL for the Arbetsförmedlingen API
    base_url = 'https://jobsearch.api.jobtechdev.se/search'

    # Search parameters for Data Engineer jobs
    search_params = {'q': "Data Engineer", 'limit': 50}

    try:
        logger.info('Fetching Data Engineer job ads from Arbetsförmedlingen API')
        
        # Make the API request
        response = requests.get(base_url, params=search_params)

        if response.status_code != 200:
            logger.error(f'Failed to fetch data. Status code: {response.status_code}')
            return []

        # Parse the JSON response and extract job ads
        job_data = response.json()
        job_ads = job_data.get('hits', [])
        logger.info(f'Successfully fetched {len(job_ads)} job ads')
        return job_ads

    except Exception as e:
        logger.error(f"Error while fetching data from the API: {e}", exc_info=True)
        return []
