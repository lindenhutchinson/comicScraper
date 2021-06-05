import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def clear():
    os.system('cls')


def get_page_soup(page_url):
    resp = requests.get(page_url)
    return BeautifulSoup(str(resp.content), "lxml")

def get_sorted_arr_from_dict(data):
    return [val for (key, val) in sorted(data.items())]


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
        "/": '',
        "\\": '',
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


def estimate_time_remaining(start_time, current, total):
    elapsed = datetime.now() - start_time
    
    seconds_per_download = elapsed.microseconds / current
    est_seconds_remaining = (total-current) * seconds_per_download
    if est_seconds_remaining >= 60:
        est_minutes_remaining = est_seconds_remaining / 60
        estimated_remaining = f"Estimated time remaining: {round(est_minutes_remaining, 1)} minutes"
    else:
        estimated_remaining = f"Estimated time remaining: {round(est_seconds_remaining, 1)} seconds"

    download_speed = f"Retrieving 1 image every {round(seconds_per_download, 1)} seconds"

    return (download_speed, estimated_remaining)


def print_progress(start_time, current, total):
    percentage = round(100*(current/total), 1)
    download_speed, estimated_remaining = estimate_time_remaining(
        start_time, current, total)
    clear()
    print(f"Currently downlading images - {percentage}%", end="\n")
    print(download_speed, end="\n")
    print(estimated_remaining, end="\n")
