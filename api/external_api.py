import aiohttp
from bot import settings
from typing import Optional

async def fetch_data(base_link: str, params: Optional[dict]) -> Optional[dict]:
    url = f"{base_link}/api/profile/get/{params["username"]}"

    try:
        async with aiohttp.ClientSession() as session:
            #GIT Request
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Error: Status code {response.status} from {url}")
                    return {}
                data = await response.json()
                
                user_info = {
                    "names": data.get("names"),
                    "pronouns": data.get("pronouns"),
                    "age": data.get("age")
                }

                return user_info
            
    except aiohttp.ClientError as e:
        print(f"API Call Error: {e}")
        return {}
    
