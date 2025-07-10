import requests
from bs4 import BeautifulSoup
import json

def scrape_episode(episode_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(episode_url, headers=headers)
    if res.status_code != 200:
        return {"error": f"Failed to fetch page: {res.status_code}"}

    soup = BeautifulSoup(res.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")
    if not script:
        return {"error": "Could not find episode data"}

    try:
        data = json.loads(script.string)
        ep_data = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['result'][0]
        return {
            "title": ep_data.get("story_title"),
            "series_title": ep_data.get("show_title"),
            "description": data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data'].get("show_desc_en"),
            "author": ep_data['user_info'].get("fullname"),
            "image": ep_data.get("image_url"),
            "plays": ep_data['stats'].get("total_plays_display"),
            "uploaded": ep_data.get("days_since_upload"),
            "duration_seconds": ep_data.get("duration"),
            "episode_id": ep_data.get("story_id"),
            "show_id": ep_data.get("show_id"),
        }
    except Exception as e:
        return {"error": str(e)}
