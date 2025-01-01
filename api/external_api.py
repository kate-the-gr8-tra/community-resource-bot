import aiohttp
from typing import Optional
import json

settings_file =  "config/settings.json"

try:
    with open(settings_file, "r") as file:
        settings = json.load(file)

except FileNotFoundError as fe:
    print(f"Error: {fe}")

async def fetch_data(base_link: str, params: Optional[dict]) -> Optional[dict]:
    username = params["username"]
    url = f"{base_link}/api/profile/get/{username}"
    data = await api_call(url)

    names = list(data["profiles"][settings["language_versions"][base_link]]["names"].keys())
    names = "/".join(names)
    pronouns = list(data["profiles"][settings["language_versions"][base_link]]["pronouns"].keys())
    pronouns = await fetch_pronoun_data(base_link, pronouns)
    age = data["profiles"][settings["language_versions"][base_link]].get("age")
    
    user_info = {
        "name": names,
        "pronouns": pronouns,
        "age": age
    }

    return user_info
        
async def fetch_pronoun_data(base_link: str, pronouns: str):
    full_pronouns = ""
    pronoun_forms = ""
    pronouns_list = pronouns.split("/")
    for i in range(len(pronouns_list)):
        pronoun_url = f"{base_link}/api/pronouns/{pronouns_list[i]}"
        data = await api_call(pronoun_url)
        if data == {}:
            continue
        form_list = list(data["morphemes"].values()) #will always be a list with 5 string elements:
        #1: subjective, 2: objective, 3: possessive det, 4: possessive, 5: reflexive
        pronoun_forms += "/".join(form_list)

        if i != 0:
            full_pronouns += ","
        if pronoun_forms not in full_pronouns:
            full_pronouns += pronoun_forms
        else:
            continue
        
    
    return full_pronouns

async def pronoun_look_up(pronoun: str):
    links = settings["language_versions"]
    for key in links.keys():
        url = f"{key}/api/pronouns"
        data = await api_call(url)
        pronouns = list(data.keys())
        for pr in pronouns:
            pronoun_forms = pronoun.split("/")
            for form in pronoun_forms:
                if pr == form:
                    return key         
    
    return None

async def api_call(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            #GIT Request
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Error: Status code {response.status} from {url}")
                    return {}
                return await response.json()

    except aiohttp.ClientError as e:
            print(f"API Call Error: {e}")
            return {}
    