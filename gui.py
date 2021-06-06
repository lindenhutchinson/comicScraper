import tkinter as tk
from chapter_controller import ChapterController
from constants import END
from comics_frame import ComicsFrame
from chapters_frame import ChaptersFrame
from tkinter import ttk


class MainApplication(tk.Frame):
    def __init__(self, master):
        self.controller = ChapterController('comics')
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_variables()
        self.create_widgets()
        

    def create_variables(self):
        self.selected_comic = tk.IntVar(self.master)
        self.selected_comic_name = tk.StringVar(self.master)
        self.selected_chapter = tk.IntVar(self.master, value=-1)
        self.selected_chapter_name = tk.StringVar(self.master)
        self.search_results = []
        self.chapter_results = []

    def perform_search(self):
        if len(self.search_results):
            self.search_results = []

        self.get_chapters_btn['state'] = "disable"
        search = self.search_input.get("1.0", END).strip('\n')
        results = self.controller.search_comics(search)
        if len(results):
            self.search_results = results
            self.search_result_box['values'] = [r['title'] for r in results]
            self.selected_comic_name.set(results[0]['title'])
            self.selected_comic.set(0)
            self.get_chapters_btn['state'] = "normal"

        # if len(results):
        #     self.search_results_frame.create_options(results)
        # else:
        #     self.search_results_frame.create_options(["No results found"])        

    def get_chapters(self):
        comic = list(filter(lambda result : result['title'] == self.selected_comic_name.get(), self.search_results))[0]
        results = self.controller.get_chapters(comic)
        self.chapter_results = results
        self.chapter_results_frame.create_options(results)

    def create_search(self):
        self.search_input = tk.Text(self.master, height=1, width=45)
        self.search_btn = tk.Button(self.master, text="Search", command=self.perform_search, width=50)
        self.search_result_box = ttk.Combobox(self.master, values=self.search_results, textvariable=self.selected_comic_name, width=55)

        self.search_input.grid(row=0, column=0, padx=10,pady=10)
        self.search_btn.grid(row=1, column=0, padx=10,pady=10)
        self.search_result_box.grid(row=2,column=0, padx=10, pady=10)

    def get_selected_comic(self):
        return self.search_results[self.selected_comic.get()]
        
    def download_chapters(self):
        chapters = self.chapter_results_frame.get_selected_options()
        selected_chapters = list(filter(lambda chapter : chapter['title'] in chapters, self.chapter_results))
        self.controller.download_some_issues(self.get_selected_comic(),selected_chapters)

    def create_chapters(self):
        self.chapter_label = tk.Label(self.master, textvariable=self.selected_comic_name)
        self.get_chapters_btn = tk.Button(self.master, text="Get chapters", command=self.get_chapters, width=50, state="disabled")
        self.chapter_results_frame = ChaptersFrame(self.master, self)
        self.chapters_download_btn = tk.Button(self.master, text="Download chapters", command=self.download_chapters, width=50)
        self.chapter_label.grid(row=3, column=0, padx=10, pady=10)
        self.get_chapters_btn.grid(row=4, column=0, padx=10, pady=10)
        self.chapter_results_frame.grid(row=5, column=0, padx=10, pady=10)
        self.chapters_download_btn.grid(row=6, column=0)

    def configure_gui(self):
        self.master.title("Comic Downloader")
        self.master.geometry("1000x1000")

    def create_widgets(self):
        self.create_search()
        # self.search_results_frame = ComicsFrame(self.master, self)
        
        self.create_chapters()




if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()

'''
TODO:
- use a combobox to select the comic
- use a listbox to select the chapters to download
- add a checkbox for choosing to download all chapters

'''