import aiohttp
from typing import Optional
import json

async def fetch_data(base_link: str, params: Optional[dict]) -> Optional[dict]:
    username = params["username"]
    url = f"{base_link}/api/profile/get/{username}"
    settings_file =  "config/settings.json"
    try:
        with open(settings_file, "r") as file:
            settings = json.load(file)
    
    except FileNotFoundError as fe:
        print(f"Error: {fe}")

    try:
        async with aiohttp.ClientSession() as session:
            #GIT Request
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Error: Status code {response.status} from {url}")
                    return {}
                data = await response.json()

                names = list(data["profiles"][settings["language_versions"][base_link]]["names"].keys())
                names = "/".join(names)
                pronouns = list(data["profiles"][settings["language_versions"][base_link]]["pronouns"].keys())
                pronouns = "/ ".join(pronouns)
                age = data["profiles"][settings["language_versions"][base_link]].get("age")
                
                user_info = {
                    "name": names,
                    "pronouns": pronouns,
                    "age": age
                }

                return user_info
            
    except aiohttp.ClientError as e:
        print(f"API Call Error: {e}")
        return {}
    

    
