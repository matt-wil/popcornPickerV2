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
    Retrieves all movie data from the OMDb API

    Parameters:
    title (str): The title of the movie to search for
    api (str): The API key to use for the OMDb API
    url (str): The URL of the OMDb API
    search_type (str): The search type to use (default "&t=")

    Returns:
    tuple: A tuple of movie data and the IMDb link for the movie

    Raises:
    ValueError: If the API key is not found
    HTTPError: If the API request returns an HTTP error
    ConnectionError: If the API request cannot connect to the API
    Timeout: If the API request times out
    RequestException: If any other error occurs during the API request
    Exception: If any other error occurs
    """
    if not api:
        logger.error(
            f"OMDB API Key not found. Check your Environment Variables")
        raise ValueError("OMDB API Key not found")

    try:
        response = requests.get(url + api + search_type + title)
        response.raise_for_status()
        movie_info = response.json()

        if movie_info.get('Response') != 'True':
            logger.error(f"Movie not found or invalid title: {title}")
            return None, None

        imdb_id = movie_info.get("imdbID")
        if not imdb_id:
            imdb_full_link = "https://www.imdb.com"
        else:
            imdb_full_link = f"https://www.imdb.com/title/{imdb_id}/"
        logger.info(f"Successfully retrieved movie data for: {title}")
        return movie_info, imdb_full_link

    except HTTPError as e:
        logger.exception(
            f"HTTP error occurred: {e} - Status Code: {response.status_code}")
    except ConnectionError as e:
        logger.exception(f"Connection Error: unable to connect to API {e}")
    except Timeout:
        logger.exception(f"Error request has timed out")
    except RequestException as e:
        logger.exception(f"Ann error occurred: {e}")
    except Exception as e:
        logger.exception(f"Key Error: {e}")

    return None, None
