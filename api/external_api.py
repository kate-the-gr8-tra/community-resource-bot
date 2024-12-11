import aiohttp
from bot import settings
from typing import Optional

API_BASE_URL = settings["api_link"]

async def fetch_data(endpoint: str, params: Optional[dict], headers: Optional[dict]):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,params=params, headers=headers) as response:
                if response.status != 200:
                    print(f"Error: Status code {response.status} from {url}")
                    return {}
                data = await response.json()
                return data
            
    except aiohttp.ClientError as e:
        print(f"API Call Error: {e}")
        return {}
    

async def get_user_data(user_id: str):
    endpoint = f"/users/{user_id}"
    data = await fetch_data(endpoint)
    return data
