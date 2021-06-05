import requests
import json


class ChapterSearcher():
    def __init__(self, base_url, search_url):
        self.search_url = search_url
        self.base_url = base_url

    def run(self, chap_name):
        resp = requests.get(f"{self.search_url}", params={'key': chap_name})
        results = json.loads(resp.content)
        search_list = []
        for res in results:
            comic = {
                'title':res['title'],
                'url':self.base_url+res['slug'],
                # 'num_chapters':res['chapters'],
                # 'released':res['released'],
                # 'notes':res['notes'],
                # 'img_url':res['img_url']
            }
            search_list.append(comic)

        return search_list

if __name__ == "__main__":
    base_url='https://wallcomic.com/comic/'
    search_url='https://wallcomic.com/ajax/search'
    # cs=ChapterSearcher(base_url, search_url)
    # results = cs.run('invincible')
    # print(json.dumps(results, separators=(',', ':'), indent=True))
