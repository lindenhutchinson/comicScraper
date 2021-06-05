import os
import requests
from bs4 import BeautifulSoup

def clear():
    os.system('cls')

def get_page_soup(page_url):
    resp = requests.get(page_url)
    return BeautifulSoup(str(resp.content), "lxml")

def get_absolute_path_to(path):
    # dirname = os.path.dirname(__file__)
    return os.path.join(os.getcwd(), path)

def fix_directory_string(string):
    fixes = {
            ' ': '_',
            ':':'',
            '.':'',
            ',':'',
            "'":'',
            '"':'',
        }
    safe_name = string.strip()
    for char, fix in fixes.items():
        string = string.replace(char, fix)

    return string
        