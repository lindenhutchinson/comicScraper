import requests
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import print_progress
from datetime import datetime

class RequestGetter():
    @staticmethod
    def runner(url_list):
        threads= []
        completed = {}
        start_time = datetime.now()
        with ThreadPoolExecutor(max_workers=20) as executor:
            for i, url in enumerate(url_list):
                threads.append(executor.submit(RequestGetter.get_response, i, url))
                
            for task in as_completed(threads):
                completed.update(task.result())

        return completed

    @staticmethod
    def get_response(num, url):
        try:
            return {num:requests.get(url, stream=True).content}
        except requests.exceptions.RequestException as e:
            print("Error trying to send a GET request to an image url", e)
