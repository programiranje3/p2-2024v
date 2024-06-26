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
    if athletes_names:
        # from_csv f. returns a list of tuples
        athletes_names = [athlete_tuple[0] for athlete_tuple in athletes_names]
    else:
        print("Getting a list of athletes' names...")
        athletes_names = scrape_athletes_names(url)
        print('...done')

        print(f'Gathered names for {len(athletes_names)} athletes.')

        to_csv(Path.cwd() / NAMES_CSV_FILE, ["athlete_name"], athletes_names)

    return athletes_names


def scrape_athletes_names(url):
    """
    Retrieves the web page with a list of top athletes,
    extracts athletes' names and returns a list of those names

    :param url: url of the page to scrape data from
    :return: a list of athletes' names
    """

    athletes_names = list()

    webdriver = get_chrome_web_driver()
    if not webdriver:
        raise RuntimeError("An error occurred while setting up web driver!")

    webdriver.get(url)
    page_content = webdriver.page_source

    page_soup = BeautifulSoup(page_content, features='html.parser')
    if not page_soup:
        raise RuntimeError(f"Could not parse content from URL: {url}. Cannot proceed!")

    div_element = page_soup.find('div', {'id':'content'})
    for li in div_element.find('ol').find_all('li'):
        strong_tag = li.find(name="strong")
        if strong_tag and strong_tag.string:
            athletes_names.append(strong_tag.string.strip())
        elif strong_tag and strong_tag.strings:
            name = list(strong_tag.stripped_strings)[-1]
            athletes_names.append(name)

    return athletes_names


def get_chrome_web_driver():
    """
    Creates and returns a Selenium web driver for Chrome web-browser

    :return: Selenium web driver for Chrome browser
    """
    options = ChromeOptions()
    options.add_argument('headless') # to prevent browser from opening when extracting content of a web page
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
        df = pd.DataFrame(data, columns=header)
        df.to_csv(fpath, index=False)
    except OSError as os_err:
        stderr.write(f"The following error occurred while writing athletes' data to file:\n{os_err}\n")


def from_csv(fpath):
    """
    Reads data from a csv file

    :param fpath: path to the csv file with the data
    :return: the content of the csv file as a list; None if, for any reason, reading from file was unsuccessful
    """
    try:
        df = pd.read_csv(fpath)
        # Option 1
        return list(df.to_records(index=False))
        # Option 2
        # return [tuple(row) for index, row in df.iterrows()]
    except OSError as os_err:
        stderr.write(f"The following error occurred while reading athletes' data from file {fpath}:\n{os_err}\n")
        stderr.write("Athletes' data will be collected again.\n")
    return None


def collect_athletes_data(athletes_names):
    """
    The function puts several parts together:
    - iterates over the list of athletes' names to retrieve the country for each
    athlete by 'consulting' their Wikipedia page
    - stores the collected data in a csv file
    - prints names of athletes whose birthplace data could not have been collected

    :param athletes_names: list with athlete names
    :return: list of athlete name and origin pairs
    """

    print("\nCollecting data about the athletes' country of origin...")

    webdriver = get_chrome_web_driver()
    if not webdriver:
        raise RuntimeError("An error occurred while setting up web driver!")

    athletes_list = list()
    not_found = list()
    for name in athletes_names:
        country = retrieve_country_of_origin(name, webdriver)
        if country:
            athletes_list.append((name, country))
        else:
            not_found.append(name)
    print('...done')

    to_csv(Path.cwd() / ORIGINS_CSV_FILE, ('athlete', 'origin'), athletes_list)

    print(f"\nInformation about country of origin was not found for the following {len(not_found)} athletes:")
    print(", ".join(not_found))

    return athletes_list


def retrieve_country_of_origin(name, web_driver):
    """
    Receives the full name of an athlete.
    Returns the country of birth of the athlete extracted from their
    Wikipedia page or None if the information is not available.

    :param name: name of an athlete
    :param web_driver: Selenium web driver to be used for scraping
    :return: country of birth (string) or None
    """

    print(f"Collecting data for {name}")

    page_url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
    web_driver.get(page_url)
    page_content = web_driver.page_source
    if not page_content:
        stderr.write(f"Could not retrieve page for: {name}\n")
        return None

    page_soup = BeautifulSoup(page_content, features='html.parser')
    if not page_soup:
        stderr.write(f"Could not parse page for: {name}\n")
        return None

    info_box = page_soup.find('table', class_=lambda c: c and 'infobox' in c and 'vcard' in c)
    if not info_box:
        if page_soup.find('div', {'id':'disambigbox'}):
            stderr.write(f"Arrived at disambiguation page for: {name}\n")
        else:
            stderr.write(f"No infobox data for: {name}\n")
        return None

    th_born = info_box.find('th', string=lambda t: t and ('born' in t.lower() or 'place of birth' in t.lower()))
    if th_born:
        td_born = th_born.find_next_sibling('td')
        if td_born and td_born.strings:
            return get_country_from_str(td_born.stripped_strings)
    else:
        bold_born = info_box.find(lambda b: b.name=='b' and b.parent.name=='td' and b.text and 'born' in b.text.lower())
        if bold_born and bold_born.parent.strings:
            return get_country_from_str(bold_born.parent.stripped_strings)

    return None


def get_country_from_str(country_string):
    complete_string = "".join(country_string)
    _, country = complete_string.rsplit(',', maxsplit=1)
    # handling situations such as U.S.[a]
    if '[' in country:
        country, _ = country.split('[')
    return country.rstrip(')').strip()


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
    athletes_dict = dict()

    country_lbls_dict = create_country_labels_mapping()
    for athlete, country in athletes_list:
        athletes_dict[athlete] = country
        for c_name, c_labels in country_lbls_dict.items():
            if country in c_labels:
                athletes_dict[athlete] = c_name
                break

    # Option 1
    from collections import defaultdict
    country_counts = defaultdict(int)
    for athlete, country in athletes_dict.items():
        country_counts[country] += 1
    # Option 2
    # from collections import Counter
    # country_counts = Counter(athletes_dict.values())

    print("Number of top athletes per country of origin:")
    for country, cnt in sorted(country_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"{country}: {cnt}")


if __name__ == '__main__':

    top_athletes_url = 'https://ivansmith.co.uk/?page_id=475'
    try:
        athletes_names = get_athletes_names(top_athletes_url)
        athletes_data = collect_athletes_data(athletes_names)
        most_represented_countries(athletes_data)
    except RuntimeError as err:
        stderr.write(f"Terminating the program due to the following runtime error:\n{err}")
