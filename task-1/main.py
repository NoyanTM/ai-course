import csv
import json
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
import httpx
from tqdm import tqdm
from fake_useragent import UserAgent

BASE_URL = "https://airkaz.org/"


def get_html(url: str) -> str:
    USER_AGENT = UserAgent().random
    response = httpx.get(url, timeout=15, headers={"User-Agent": USER_AGENT})
    if response.status_code == 200:
        return response.text
    return None


def extract_cities_links(html_data: str, soup_context: BeautifulSoup) -> list[str]:
    city_links = []
    menu = soup_context.find('ul', class_='dropdown-menu')
    if menu:
        links = menu.find_all('a', href=True)
        cities = [link['href'] for link in links]
        city_links = [BASE_URL + city for city in cities]
    return city_links


def extract_sensors_data(soup_context: BeautifulSoup) -> list[dict]:
    script_tag = soup_context.find('script', string=lambda t: t and 'sensors_data' in t)

    if script_tag:
        script_content = script_tag.string

    start_index = script_content.find('[')
    end_index = script_content.rfind(']') + 1

    json_data = script_content[start_index:end_index]
    sensors_data = json.loads(json_data)
    return sensors_data


def parse_data():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_data = get_html(BASE_URL)
    soup = BeautifulSoup(html_data, 'lxml')
    
    city_links = extract_cities_links(html_data, soup)
    
    html_pages = []
    for link in tqdm(city_links, desc="Fetching city pages", unit="city"):
        page = get_html(link)
        html_pages.append(page)
    
    sensors_data = []
    for page in tqdm(html_pages, desc="Extracting sensor data", unit="page"):
        soup = BeautifulSoup(page, 'lxml')
        data = extract_sensors_data(soup)
        sensors_data.extend(data)
    
    json_data = json.dumps(sensors_data, indent=4, ensure_ascii=False)
    df = pd.read_json(json_data, orient="records")
    df.to_csv(f"./data/sensors_data_{time_now}.csv", index=False)
    with open(f"./data/sensors_data_{time_now}.json", "w") as file:
        file.write(json_data)
