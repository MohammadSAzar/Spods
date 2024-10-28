import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from bs4 import BeautifulSoup


# --------------------------------- Real Scraping ---------------------------------
category_url_list = [
    'https://castbox.fm/categories/10021?country=ir',  # Arts
    'https://castbox.fm/categories/10028?country=ir',  # Business
    'https://castbox.fm/categories/10035?country=ir',  # Comedy
    'https://castbox.fm/categories/10039?country=ir',  # Education
    'https://castbox.fm/categories/10044?country=ir',  # Fiction
    'https://castbox.fm/categories/10048?country=ir',  # Leisure
    'https://castbox.fm/categories/10057?country=ir',  # Government
    'https://castbox.fm/categories/10058?country=ir',  # History
    'https://castbox.fm/categories/10059?country=ir',  # Health & Fitness
    'https://castbox.fm/categories/10066?country=ir',  # Kids & Family
    'https://castbox.fm/categories/10071?country=ir',  # Music
    'https://castbox.fm/categories/10075?country=ir',  # News
    'https://castbox.fm/categories/10083?country=ir',  # Religion & Spirituality
    'https://castbox.fm/categories/10091?country=ir',  # Science
    'https://castbox.fm/categories/10101?country=ir',  # Society & Culture
    'https://castbox.fm/categories/10107?country=ir',  # Sports
    'https://castbox.fm/categories/10123?country=ir',  # Technology
    'https://castbox.fm/categories/10124?country=ir',  # True Crime
    'https://castbox.fm/categories/10125?country=ir',  # TV & Film
]
CASTBOX_BASE_URL = 'https://castbox.fm'


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# Set up retries with backoff strategy
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))


# Scrape data from each podcast URL
def scrape_data_from_podcast_url(url):
    if not url.startswith("http"):
        url = CASTBOX_BASE_URL + url

    try:
        response = session.get(url, headers=HEADERS, timeout=10, verify=True)  # Set verify to True for SSL
        response.raise_for_status()
    except requests.exceptions.SSLError as ssl_error:
        print(f"SSL error encountered for {url}: {ssl_error}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to access {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    cover = soup.find('img', class_='img')['src']
    title = soup.find('h1', class_='ch_feed_info_title').text.strip()
    creator = soup.find('p', class_='author').text.strip()
    subscribed = soup.find('span', class_='count sub_count').text.strip()
    played = soup.find('span', class_='count play_count').text.strip()
    description = soup.find('div', class_='des-con').text.strip()

    return {
        'cover': cover,
        'title': title,
        'creator': creator,
        'subscribed': subscribed,
        'played': played,
        'description': description
    }


# Scrape all podcasts from a single category page
def scrape_category_podcast(category_url):
    try:
        response = session.get(category_url, headers=HEADERS, timeout=10, verify=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to access {category_url}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    podcast_links = []
    for div in soup.find_all('div', class_='bottomCon clearfix'):
        a_tag = div.find('a')
        if a_tag:
            podcast_links.append(a_tag['href'])

    podcasts = []
    for link in podcast_links:
        pod_data = scrape_data_from_podcast_url(link)
        if pod_data:
            podcasts.append(pod_data)

    return podcasts


# Scrape all podcasts from the list of category URLs
def scrape_all_podcasts(input_list):
    all_podcast_data = []
    for url in input_list:
        podcasts_on_page = scrape_category_podcast(url)
        all_podcast_data.extend(podcasts_on_page)
    return all_podcast_data


# Usage
podcast_data = scrape_all_podcasts(category_url_list)
print('POD: ', podcast_data)
print('POD: ', len(podcast_data))





