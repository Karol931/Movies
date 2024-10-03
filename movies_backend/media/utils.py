
import requests
from bs4 import BeautifulSoup
import re


def get_movie_data(tmdb_id):
    url = 'https://www.themoviedb.org/movie/' + tmdb_id + '/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')

    return soup

def get_tv_show_data(tmdb_id):
    url = 'https://www.themoviedb.org/tv/' + tmdb_id + '/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')

    return soup

def get_seasons_data(tmdb_id):
    url = 'https://www.themoviedb.org/tv/' + tmdb_id + '/seasons'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')

    return soup


def get_episodes_data(tmdb_id, season):
    url = 'https://www.themoviedb.org/tv/' + tmdb_id + '/season/' + str(season)
    source = requests.get(url).text

    soup = BeautifulSoup(source, 'html.parser')

    return soup


def get_movie_parameters(tmdb_id):
    soup = get_movie_data(tmdb_id)
    # get movie title
    title = get_media_title(soup)
    # get movie img src
    img = get_media_image(soup)
    # get movie description
    description = get_media_description(soup)

    return title, img, description


def get_tv_show_parameters(tmdb_id):
    soup = get_tv_show_data(tmdb_id)

    title = get_media_title(soup)
    img = get_media_image(soup)
    description = get_media_description(soup)

    soup = get_seasons_data(tmdb_id)
    seasons_number = get_tv_show_seasons_number(soup)

    soup = get_episodes_data(tmdb_id, seasons_number)

    seasons = [
        {'season_number': season, 'episodes': [{'title': get_episode_title(get_episodes_data(tmdb_id, season), episode), 'episode_number': episode } for episode in range(1,int(get_episodes_number(get_episodes_data(tmdb_id, season)))+1)]} for season in range(1,int(seasons_number) + 1)
    ]
    print(seasons)
    return title, img, description, seasons

def get_media_title(soup):
    try:
        title = soup.find('h2').text.split('(')[0].strip()
    except:
        title = None
    
    return title


def get_media_image(soup):
    try:
        pattern = r'src="(.*?)"'
        match = re.search(pattern, str(soup.find_all('img')[1]))
        img = match.group(1)
    except:
        img = None
    
    return img


def get_media_description(soup):
    try:
        description = soup.find_all('p')[2].text
    except:
        description = None
    
    return description


def get_tv_show_seasons_number(soup):
    try:
        seasons_number = soup.find_all('h2')[-1].text.split(' ')[1]
    except:
        seasons_number = None

    return seasons_number


def get_episodes_number(soup):
    try:
        episode_number = soup.find(class_='episode_sort').text.split(' ')[1]
    except:
        episode_number = None

    return episode_number


def get_episode_title(soup, episode_number):
    try:
        episode_title = soup.find_all(class_='episode_title')[episode_number-1].findChild('h3').text
    except:
        episode_title = None

    return episode_title
