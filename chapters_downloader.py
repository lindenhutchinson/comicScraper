from chapter_maker import ChapterMaker
from utils import clear, get_page_soup, fix_directory_string, ensure_directory_exists


class ChaptersDownloader():
    '''
    params:
        url<str>: the url containing a list of chapters
        dir<str>: the directory to save the chapters into, with a trailing /

    '''

    def __init__(self, url, title):
        self.url = url
        self.title = title

    def get_chapter_urls(self):
        '''
        fetches a dictionary of chapter_title:chapter_url

        returns:
            dict<chap_name:url>: A dictionary that uses the chapter name as the key, and the issue url as the value
        '''
        soup = get_page_soup(self.url)
        div = soup.find(class_="episode-list")

        chap_urls = {}
        for chap in div.find_all("a"):
            href = chap['href']
            if href not in chap_urls:
                chap_name = chap.get_text()
                # add /all to this when you want to stop debugging!!!!!
                chap_urls.update({chap_name: href})

        return chap_urls

    def download_all(self, directory):
        """
        For downloading all chapters that have been found
        """     
        self.download_some(directory, self.get_chapter_urls())

    def download_some(self, directory, chap_urls):
        dir = ensure_directory_exists(directory, self.title)
        for chap_name, url in chap_urls.items():
            cm = ChapterMaker(chap_name, url)
            chap_name = fix_directory_string(chap_name)
            path = f"{dir}\\{chap_name}"
            cm.create_pdf(f"{path}.pdf")


if __name__ == "__main__":
    cd = ChaptersDownloader(
        'https://wallcomic.com/comic/doomsday-clock', './comics/')
    cd.run()
