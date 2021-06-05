from chapter_searcher import ChapterSearcher
from chapters_downloader import ChaptersDownloader
import os
from utils import get_absolute_path_to, ensure_directory_exists


class ChapterController():
    def __init__(self, save_dir):
        ensure_directory_exists('.', save_dir)
        self.save_dir = get_absolute_path_to(save_dir)

    def search_comics(self, search):
        searcher = ChapterSearcher()
        results = searcher.run(search)
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

    def present_options(self, options):
        choice = -1
        while(not(0 <= choice <= len(options))):
            try:
                prompt = "\n".join(
                    [f"{i} - {opt}" for i, opt in enumerate(options)])
                choice = int(input(prompt))
                if not (0 <= choice <= len(options)):
                    print(
                        f"Sorry, I couldn't understand that input, try entering a number between 0 or a {len(options)}")
                    choice = -1
                    continue
            except ValueError:
                print("You need to enter a number!")
                continue

        return choice

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

            continue_downloading = self.present_options([
                "Search for a different comic",
                "Download a comic from the list"
            ])

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
                
                download_all = self.present_options([
                    'Choose chapters to download',
                    'Download all issues'
                ])
                if download_all:
                    self.download_all_issues(comic)
                else:
                    options, chap_urls = self.get_chapters(comic)
                    print("\n".join(options))
                    d_chaps_input = input("Enter the chapter ID's for those you would like to download, separated by a comma")
                    d_chaps = d_chaps_input.split(',')
                    print("Choose an issue to download")

            go = False

        self.get_user_input()

'''
TODO: CHAPTER GUI
- input for chapter search
- display results from chapter search
- select comic from chapter search
- display selected comic chapters
- select chapters to download
- input for save directory (default comics)
- use constants for BASE_URL and SEARCH_URL
- download chapters
- merging chapters option added eventually




'''
if __name__ == "__main__":
    # base_url = 'https://wallcomic.com/comic/'
    # search_url = 'https://wallcomic.com/ajax/search'
    save_dir = "comics"
    cc = ChapterController(save_dir)
    cc.get_user_input()
