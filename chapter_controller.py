from chapter_searcher import ChapterSearcher
from chapters_downloader import ChaptersDownloader
import os 
from utils import get_absolute_path_to, fix_directory_string


class ChapterController():
    def __init__(self, save_dir, base_url, search_url):
        self.save_dir = get_absolute_path_to(save_dir)
        self.search = ChapterSearcher(base_url, search_url)

    def search_comics(self, search):
        results = self.search.run(search)
        options = [f"{i}: {c['title']}" for i, c in enumerate(results)]
        return (options, results)

    def ensure_comic_directory(self, comic_name):

        safe_name = fix_directory_string(comic_name)
        dir = f"{self.save_dir}/{safe_name}"
        try:
            os.mkdir(dir)
            print(f"created directory: {dir}")
        except OSError as e:
            # print(e)
            print(f"{dir} already exists, no need to create it")

        return dir 

    def download_comic(self, comic):
        cd = ChaptersDownloader(comic['url'], comic['title'])
        cd.run()

    def get_user_input(self):
        go = True
        while go:
            search = input("Search for a comic:\n")
            options, results = self.search_comics(search)
            if len(options):
                print(f"Here are the results for your search:", end="\n\n")
                print(options, sep="\n\n", end="\n\n")
            else:
                print("Sorry, I didn't find any results for that search")
                go = False

            if input("0: Search for a different comic\n1: Download a comic from the list\n"):
                try:
                    comic_num = int(input("Enter the number for the comic you would like to download:\n"))
                except ValueError:
                    print("You need to enter a number!!!")
                    go = False
                    continue

                comic = results[comic_num]
                dir = self.ensure_comic_directory(comic['title'])
                cd = ChaptersDownloader(comic['url'], dir)
                cd.run()


            go = False

        self.get_user_input()



        


if __name__ == "__main__":
    base_url='https://wallcomic.com/comic/'
    search_url='https://wallcomic.com/ajax/search'
    save_dir = "comics\\"
    cc = ChapterController(save_dir,base_url, search_url)
    cc.get_user_input()
 