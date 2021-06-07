import requests
import json

BASE_URL = 'https://wallcomic.com/comic/'
SEARCH_URL = 'https://wallcomic.com/ajax/search'

class ChapterSearcher():
    def __init__(self):
        self.search_url = SEARCH_URL
        self.base_url = BASE_URL

    def run(self, chap_name):
        resp = requests.get(self.search_url, params={'key': chap_name})
        results = json.loads(resp.content)
        search_list = []
        for res in results:
            comic = {
                'title': res['title'],
                'url': self.base_url+res['slug'],
                # 'num_chapters':res['chapters'],
                # 'released':res['released'],
                # 'notes':res['notes'],
                # 'img_url':res['img_url']
            }
            search_list.append(comic)

        return search_list


if __name__ == "__main__":
    # base_url='https://wallcomic.com/comic/'
    # search_url='https://wallcomic.com/ajax/search'
    cs=ChapterSearcher()
    results = cs.run('invincible')
    print(json.dumps(results, separators=(',', ':'), indent=True))
