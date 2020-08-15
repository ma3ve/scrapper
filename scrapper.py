import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

print('search:')
search = '+'.join(input().split(" "))

software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value,
                     OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=1)
user_agent = user_agent_rotator.get_random_user_agent()
headers = {"User-Agent": user_agent}


res = requests.get(f"https://www.amazon.in/s?k={search}", headers=headers)
data = BeautifulSoup(res.content, 'lxml')
items = data.find_all(class_="s-result-item")

results = []

for item in items:
    try:
        brand = None
        if(item.find('h5', class_='s-line-clamp-1')):
            brand = item.find('h5', class_='s-line-clamp-1').span.text
            title = item.find(
                'h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2').span.text

        else:
            title = item.find(
                'span', class_='a-size-medium a-color-base a-text-normal').text
        result = {
            "cost": item.find(class_="a-price-whole").text,
            "image": item.find('img')['src'],
            "ratings": item.find('span', class_='a-icon-alt').text,
            "title": title,
            "brand": brand
        }
        results.append(result)
    except:
        pass


print({"results": results})
