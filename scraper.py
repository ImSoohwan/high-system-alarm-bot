import aiohttp
from bs4 import BeautifulSoup

api_url = "..."
headers = {
    ...
}
payload = {
    "pageIndex": "1",
    "ablityCategory": "ALL",
    "addFavorite": "",
    "npiPartiDeptCd": "",
    "npiOprtDeptCdNm": "",
    "addReqOrdFlag": "",
    "addReqDeadLine": "",
    "npiTitle": "",
    "listType": "CARD"
}

def check_keyword(keyword, info_list):
    for info in info_list:
        found = False
        found = any(keyword in el.get_text() for el in info)
        if found: break
    return found

async def start_scraping(keywords):
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=payload) as res:
            if res.status == 200:
                text = await res.text()
                soup = BeautifulSoup(text, "html.parser")
                info_list = soup.select("dl.program_infolist")
                result = []
                for keyword in keywords:
                    result.append((keyword, check_keyword(keyword, info_list)))
                return result
    return []
