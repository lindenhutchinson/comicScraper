from .chapter_maker import ChapterMaker
from .utils import clear, get_page_soup, fix_directory_string, ensure_directory_exists, get_sorted_arr_from_dict, reverse_dict
import re
from .request_getter import RequestGetter
from bs4 import BeautifulSoup

class ChaptersDownloader():
    '''
    params:
        url<str>: the url containing a list of chapters
        dir<str>: the directory to save the chapters into, with a trailing /

    '''

    def __init__(self, url, title, verbose=False):
        self.url = url
        self.title = title
        self.verbose = verbose


    def recur_paginate(self, url, url_list):
        soup = get_page_soup(url)
        pagination = soup.find('a', rel="next")
        if pagination:
            url = re.sub(r'(\?page=\d+)', '', url)
            page = re.findall(r'(\?page=\d+)', pagination['href'])[0]
            next_url = url+page
            url_list.append(next_url)
            return self.recur_paginate(next_url, url_list)

        return url_list

    def get_chapter_urls(self):
        '''
        fetches a dictionary of chapter_title:chapter_url

        returns:
            dict<chap_name:url>: A dictionary that uses the chapter name as the key, and the issue url as the value
        '''
        soup = get_page_soup(self.url)
        pagination = soup.find('a', rel="next")

        url_list = self.recur_paginate(self.url, [self.url])
        chap_urls = {}
        pages_content = RequestGetter.runner(url_list)
        pages_content = get_sorted_arr_from_dict(pages_content)
        for page in pages_content:
            soup = BeautifulSoup(str(page), "lxml")

            div = soup.find(class_="episode-list")

            for chap in div.find_all("a"):
                href = chap['href']
                if href not in chap_urls:
                    chap_name = chap.get_text()
                    chap_urls.update({chap_name: href+'/all'})
        if self.verbose:
            print(f"I found {len(list(chap_urls.items()))} chapters")
        return reverse_dict(chap_urls)
        # reverse the chapter list as it is listed from most recently released on the website but we want in order of release

    def download_all(self, directory):
        """
        For downloading all chapters that have been found
        """     
        self.download_some(directory, self.get_chapter_urls())

    def download_some(self, directory, chap_urls):
        dir = ensure_directory_exists(directory, self.title)
        broken_chapters = []
        for chap in chap_urls: 
            cm = ChapterMaker(chap['title'], chap['href'], self.verbose)
            chap_name = fix_directory_string(chap['title'])
            path = f"{dir}\\{chap_name}"
            res = cm.create_pdf(f"{path}.pdf")
            if not res:
                broken_chapters.append(chap['title'])

        return broken_chapters


if __name__ == "__main__":
    url = 'https://wallcomic.com/comic/uncanny-x-men-1963'
    title = 'test-title'
    save_dir = 'test'
    cd = ChaptersDownloader(url, title)
    cd.download_all(save_dir)
