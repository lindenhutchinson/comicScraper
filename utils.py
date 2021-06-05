import os
import requests
from bs4 import BeautifulSoup


def clear():
    os.system('cls')


def get_page_soup(page_url):
    resp = requests.get(page_url)
    return BeautifulSoup(str(resp.content), "lxml")


def get_absolute_path_to(path):
    return os.path.join(os.getcwd(), path)


def fix_directory_string(string):
    fixes = {
        ' ': '_',
        ':': '',
        '.': '',
        ',': '',
        "'": '',
        '"': '',
        "/":'',
        "\\":'',
    }
    safe_name = string.strip()
    for char, fix in fixes.items():
        string = string.replace(char, fix)

    return string


def ensure_directory_exists(base_dir, new_folder):
    safe_name = fix_directory_string(new_folder)
    dir = f"{base_dir}\\{safe_name}"
    try:
        os.mkdir(dir)
        print(f"created directory: {dir}")
    except OSError as e:
        # print(e)
        print(f"{dir} already exists, no need to create it")

    return dir
