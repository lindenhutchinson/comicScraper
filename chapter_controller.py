from chapter_searcher import ChapterSearcher
from chapters_downloader import ChaptersDownloader
import os
from utils import get_absolute_path_to, ensure_directory_exists


class ChapterController():
    def __init__(self, save_dir, base_url, search_url):
        self.save_dir = get_absolute_path_to(save_dir)
        self.search = ChapterSearcher(base_url, search_url)

    def search_comics(self, search):
        results = self.search.run(search)
        options = [f"{i}: {c['title']}" for i, c in enumerate(results)]
        return (options, results)

    def get_chapters(self, comic):
        cd = ChaptersDownloader(comic['url'], comic['title'])
        chap_urls = cd.get_chapter_urls()
        options = [f"{i}: {c['title']}" for i, c in enumerate(chap_urls)]
        return (options, chap_urls)

    def download_all_issues(self, comic):
        cd = ChaptersDownloader(comic['url'], comic['title'])
        cd.download_all(self.save_dir)

    def download_some_issues(self, chap_urls):
        cd = ChaptersDownloader(comic['url'], comic['title'])
        cd.download_some(self.save_dir, chap_urls)

    def get_user_input(self):
        go = True
        while go:
            search = input("Search for a comic: ")
            options, results = self.search_comics(search)
            if len(options):
                print(f"Here are the results for your search:", end="\n\n")
                print(options, sep="\n\n", end="\n\n")
            else:
                print("Sorry, I didn't find any results for that search")
                go = False
                continue
            continue_downloading = -1
            while(not(0<=continue_downloading<= 1)):
                try:
                    continue_downloading = int(
                        input("0: Search for a different comic\n1: Download a comic from the list\n:"))
                    if not (0 <= continue_downloading <= 1):
                        print("Sorry, I couldn't understand that input, try entering a 0 or a 1")
                        continue_downloading = -1
                        continue
                except ValueError:
                    print("You need to enter a number!")
                    continue

            if continue_downloading:
                try:
                    comic_num = int(
                        input("Enter the number for the comic you would like to download: "))
                except ValueError:
                    print("You need to enter a number!")
                    go = False
                    continue
                try:
                    comic = results[comic_num]
                except IndexError:
                    print("Couldn't find a comic with that ID")
                    go = False
                    continue

                self.download_all_issues(comic)

            go = False

        self.get_user_input()


if __name__ == "__main__":
    base_url = 'https://wallcomic.com/comic/'
    search_url = 'https://wallcomic.com/ajax/search'
    save_dir = "comics"
    ensure_directory_exists('.', 'comics')
    cc = ChapterController(save_dir, base_url, search_url)
    cc.get_user_input()
