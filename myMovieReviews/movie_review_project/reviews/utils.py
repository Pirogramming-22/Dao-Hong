#import requests
from decouple import config

def fetch_movie_details(title):
    """Fetch movie details from TMDB API based on title."""
    api_key = config('TMDB_API_KEY')
    base_url = "https://api.themoviedb.org/3"
    search_url = f"{base_url}/search/movie"
    details = {}

    # Step 1: Search for the movie by title
    search_params = {
        "api_key": api_key,
        "query": title,
        "language": "ko-KR"  # Set language to Korean for localized results
    }
    search_response = requests.get(search_url, params=search_params)
    if search_response.status_code == 200:
        search_results = search_response.json().get("results")
        if search_results:
            # Get the first result
            movie_id = search_results[0].get("id")
            details["title"] = search_results[0].get("title")
            details["release_year"] = search_results[0].get("release_date", "")[:4]
            details["image"] = f"https://image.tmdb.org/t/p/w500{search_results[0].get('poster_path')}"

            # Step 2: Fetch movie details for additional data
            movie_details_url = f"{base_url}/movie/{movie_id}"
            movie_details_params = {"api_key": api_key, "language": "ko-KR"}
            details_response = requests.get(movie_details_url, params=movie_details_params)
            if details_response.status_code == 200:
                movie_details = details_response.json()
                details["director"] = next(
                    (person["name"] for person in movie_details.get("credits", {}).get("crew", [])
                     if person["job"] == "Director"), "정보 없음"
                )
                details["main_cast"] = ", ".join([
                    cast["name"] for cast in movie_details.get("credits", {}).get("cast", [])[:3]
                ])
                details["runtime"] = movie_details.get("runtime", 0)

    print(details)
    return details
