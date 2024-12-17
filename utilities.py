import requests
import os
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from datamanager.sqliteDataManager import logger

# access environment variable for api_key
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OMDB_API_KEY")
OMDb_url = "http://www.omdbapi.com/?apikey="


def retrieve_all_movie_data(title, api=api_key, url=OMDb_url, search_type="&t="):
    """
    Returns the response from the OMDB API plus and full link for the movie
    :param title: Title of the movie
    :param api:
    :param url:
    :param search_type:
    :return:
    """
    try:
        response = requests.get(url + api + search_type + title)
        response.raise_for_status()
        movie_info = response.json()
        imdb_id = movie_info["imdbID"]
        imdb_full_link = f"https://www.imdb.com/title/{imdb_id}/"
        return movie_info, imdb_full_link
    except HTTPError as e:
        print(
            f"HTTP error occurred: {e} - Status Code: {response.status_code}")
        logger.exception(f"HTTP error occurred: {e} - Status Code: {response.status_code}")
    except ConnectionError as e:
        print(f"Connection Error: unable to connect to API {e}")
        logger.exception(f"Connection Error: unable to connect to API {e}")
    except Timeout:
        print(f"Error request has timed out")
        logger.exception(f"Error request has timed out")
    except RequestException as e:
        print(f"Ann error occurred: {e}")
        logger.exception(f"Ann error occurred: {e}")
