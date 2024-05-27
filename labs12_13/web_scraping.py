"""
LABs 12 & 13
"""

"""
Potrebno je napisati Python program (skriptu) koji određuje koje zemlje
su dale veliki broj sportista i sportistkinja koji se smatraju među 100 
najvećih sportistskih zvezda vremena. 
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
from sys import stderr
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

ORIGINS_CSV_FILE = "athletes_origin.csv"
NAMES_CSV_FILE = "athletes_names.csv"


def get_athletes_names(url):
    """
    The function, first, tries to load the data (athletes' names) from a local file;
    if the file does not exist (= data was not collected yet), it collects the
    data by calling the scrape_athletes_names() f. and stores the collected data
    for potential later use; the data is also returned as a list of athletes' names

    :param url: url of the page to scrape data from
    :return: a list of athletes' names
    """
    pass


def scrape_athletes_names(url):
    """
    Retrieves the web page with a list of top athletes,
    extracts athletes' names and returns a list of those names

    :param url: url of the page to scrape data from
    :return: a list of athletes' names
    """
    pass


def get_chrome_web_driver():
    """
    Creates and returns a Selenium web driver for Chrome web-browser

    :return: Selenium web driver for Chrome browser
    """
    pass


def to_csv(fpath, header, data):
    """
    Auxiliary function for storing the collected data in a csv file

    :param fpath: path to the file where data will be stored
    :param header: header (variable names) of the csv file; expected as a list, tuple, or an iterable
    :param data: data to store; expected as a list or a tuple
    :return: nothing
    """
    pass


def from_csv(fpath):
    """
    Reads data from a csv file

    :param fpath: path to the csv file with the data
    :return: the content of the csv file as a list; None if, for any reason, reading from file was unsuccessful
    """
    pass


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
    pass


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

    pass

    # top_athletes_url = 'https://ivansmith.co.uk/?page_id=475'
    # try:
    #     athletes_names = get_athletes_names(top_athletes_url)
    #     # athletes_data = collect_athletes_data(athletes_names)
    #     # most_represented_countries(athletes_data)
    # except RuntimeError as err:
    #     stderr.write(f"Terminating the program due to the following runtime error:\n{err}")