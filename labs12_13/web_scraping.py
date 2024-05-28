"""
LABs 12 & 13
"""

"""
Potrebno je napisati Python program (skriptu) koji određuje koje zemlje
su dale veliki broj sportista i sportistkinja koji se smatraju među 100 
najvećih sportistskih zvezda svih vremena. 
Konkretno, program bi trebalo da uradi sledeće:
- Prikupi imena sportista i sportistkinja sa Web stranice 
  "100 Greatest Sports Stars Ever": https://ivansmith.co.uk/?page_id=475
- Za svakog identifikovanog sportistu / sportistkinju, odredi zemlju rođenja 
  preuzimajući relevantne podatke (mesto rođenja) sa njihove Wikipedia stranice
- Sačuva podatke o sportistima / sportistkinjama i njihovoj zemlji porekla 
  u csv fajlu (u formatu "athlete, origin")
- Prikaže sortiranu listu identifikovanih zemalja i za svaku zemlju broj
  najvećih sportistskih zvezda koje je dala.

Napomene: 
Da bismo pristupili sadržaju Web stranica, koristićemo Web drajvere 
iz Selenium biblioteke (https://www.selenium.dev/documentation/webdriver/)

Dokumentacija za Selenium WebDriver za Chrome browser je dostupna na: 
https://www.selenium.dev/documentation/webdriver/browsers/chrome/

Dokumentacija za BeautifulSoup je dostupna na:
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from sys import stderr
from pathlib import Path
import pandas as pd

ORIGINS_CSV_FILE = "athletes_origin.csv"
NAMES_CSV_FILE = "athletes_names.csv"


def get_athletes_names(url):
    """
    The function, first, tries to load the data (athletes' names) from a local file (NAMES_CSV_FILE);
    if the file does not exist (= data was not collected yet), it collects the
    data by calling the scrape_athletes_names() f. and stores the collected data
    for potential later use; the data is also returned as a list of athletes' names

    :param url: url of the page to scrape data from
    :return: a list of athletes' names
    """
    athletes_names = from_csv(Path.cwd() / NAMES_CSV_FILE)
    if not athletes_names:
        print(f"Collecting athletes' names from the following web page: {url}")
        athletes_names = scrape_athletes_names(url)
        print(f"... done")

        to_csv(Path.cwd() / NAMES_CSV_FILE, ['athlete_name'], athletes_names)
    else:
        athletes_names = [athlete[0] for athlete in athletes_names]

    return athletes_names


def scrape_athletes_names(url):
    """
    Retrieves the web page with a list of top athletes,
    extracts athletes' names and returns a list of those names

    :param url: url of the page to scrape data from
    :return: a list of athletes' names
    """
    chrome_webdriver = get_chrome_web_driver()
    chrome_webdriver.get(url)
    page_content = chrome_webdriver.page_source
    if not page_content:
        raise RuntimeError(f"Could not collect athletes' names from {url}. Cannot proceed!")

    page_soup = BeautifulSoup(page_content, "html.parser")
    if not page_soup:
        raise RuntimeError(f"Could not parse the content from the given web page ({url}). Cannot proceed!")

    atheletes_names = []
    content_div = page_soup.find(name='div', attrs={'id':'content'})
    list_items = content_div.find(name='ol').find_all(name="li")
    for list_item in list_items:
        strong_tag = list_item.find(name="strong")
        if strong_tag and strong_tag.string:
            # atheletes_names.append(strong_tag.text.strip())
            atheletes_names.append(strong_tag.string.strip())
        elif strong_tag and strong_tag.strings:
            atheletes_names.append(list(strong_tag.stripped_strings)[-1])

    return atheletes_names


def get_chrome_web_driver():
    """
    Creates and returns a Selenium web driver for Chrome web-browser

    :return: Selenium web driver for Chrome browser
    """
    options = ChromeOptions()
    options.add_argument("headless")
    return webdriver.Chrome(options=options)


def to_csv(fpath, header, data):
    """
    Auxiliary function for storing the collected data in a csv file

    :param fpath: path to the file where data will be stored
    :param header: header (variable names) of the csv file; expected as a list, tuple, or an iterable
    :param data: data to store; expected as a list or a tuple
    :return: nothing
    """
    try:
        df = pd.DataFrame(data=data, columns=header)
        df.to_csv(fpath, index=False)
    except OSError as os_err:
        stderr.write(f"Error occurred when trying to write data to csv file {fpath}:\n{os_err}\n")


def from_csv(fpath):
    """
    Reads data from a csv file

    :param fpath: path to the csv file with the data
    :return: the content of the csv file as a list; None if, for any reason, reading from file was unsuccessful
    """
    df = pd.read_csv(fpath)
    # return [tuple(row) for index, row in df.iterrows()]
    return list(df.to_records(index=False))


def collect_athletes_data(athletes_names):
    """
    The function puts several parts together:
    - iterates over the list of athletes' names to retrieve the country for each
    athlete by 'consulting' their Wikipedia page
    - stores the collected data in a json file
    - prints names of athletes whose birthplace data could not have been collected

    :param athletes_names: list with athlete names
    :return: list of athlete name and origin pairs
    """



def retrieve_country_of_origin(name, web_driver):
    """
    Receives the full name of an athlete.
    Returns the country of birth of the athlete extracted from their
    Wikipedia page or None if the information is not available.

    :param name: name of an athlete
    :param web_driver: Selenium web driver to be used for scraping
    :return: country of birth (string) or None
    """
    pass


def create_country_labels_mapping():
    """
    Creates a mapping between a country and different ways it was referred to
    in the collected data

    :return: a dictionary with countries as the keys and lists of different terms
    used to refer to them as values
    """

    country_lbls_dict = dict()

    country_lbls_dict['USA'] = ['California', 'New York', 'United States', 'Florida', 'Oklahoma', 'US', 'U.S.',
                                'Pennsylvania', 'Ohio', 'Mississippi', 'Alabama', 'Indian Territory', 'Maryland']
    country_lbls_dict['Germany'] = ['West Germany']
    country_lbls_dict['Australia'] = ['Victoria', 'Western Australia', 'New South Wales']
    country_lbls_dict['UK'] = ['England', 'UK', 'British Leeward Islands', 'United Kingdom', 'Northern Ireland']

    return country_lbls_dict


def most_represented_countries(athletes_list):
    """
    Creates and prints a list of countries based on how well they
    are represented in the collected athletes data
    
    :param athletes_list: list of athlete name and origin pairs
    :return: nothing
    """
    pass


if __name__ == '__main__':

    top_athletes_url = 'https://ivansmith.co.uk/?page_id=475'
    try:
        athletes_names = get_athletes_names(top_athletes_url)
        # athletes_data = collect_athletes_data(athletes_names)
        # most_represented_countries(athletes_data)
    except RuntimeError as err:
        stderr.write(f"Terminating the program due to the following runtime error:\n{err}")