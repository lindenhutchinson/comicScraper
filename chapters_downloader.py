from chapter_maker import ChapterMaker
from utils import clear, get_page_soup, fix_directory_string


class ChaptersDownloader():
    '''
    params:
        url<str>: the url containing a list of chapters
        dir<str>: the directory to save the chapters into, with a trailing /

    '''

    def __init__(self, url, dir):
        self.url = url
        self.dir = dir

    def get_chapter_urls(self):
        '''
        fetches a list of chapter urls that can iterated over to download all chapters

        returns:
            list<str>: list of chapter urls

        '''
        soup = get_page_soup(self.url)
        div = soup.find(class_="episode-list")

        chap_urls = {}
        for chap in div.find_all("a"):
            href = chap['href']
            if href not in chap_urls:
                title = chap.get_text()
                chap_urls.update({title: f"{href}"}) # add /all to this when you want to stop debugging!!!!!

        return chap_urls

    def run(self):
        chap_urls = self.get_chapter_urls()
        for title, url in chap_urls.items():
            cm = ChapterMaker(title, url)
            path = fix_directory_string(f"{self.dir}\\{title}")
            cm.create_pdf(f"{path}.pdf")


if __name__ == "__main__":
    cd = ChaptersDownloader('https://wallcomic.com/comic/doomsday-clock', './comics/')
    cd.run()

