import tkinter as tk
from tkinter import ttk
from threading import Thread
import queue

from scraping.chapter_controller import ChapterController
from chapters_frame import ChaptersFrame


class GuiController:
    def __init__(self):
        self.controller = ChapterController('comics', False)

    def search_comics(self, **kwargs):
        results = self.controller.search_comics(kwargs.get('search_input'))
        kwargs.get('thread_queue').put(results)

    def get_chapters(self, **kwargs):
        results = self.controller.get_chapters(kwargs.get('comic'))
        kwargs.get('thread_queue').put(results)

    def download_chapters(self, **kwargs):
        results = self.controller.download_some_issues(kwargs.get('comic'), kwargs.get('chapters'))
        kwargs.get('thread_queue').put(results)



class MainApplication(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.ctrl = GuiController()
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_variables()
        self.create_widgets()
        self.place_widgets()
        self.thread_queue = queue.Queue()

    def listen_for_result(self, output_func):
        try:
            item = self.thread_queue.get(0)
            output_func(item)
        except queue.Empty:
            self.after(100, self.listen_for_result, output_func)

    def run_in_new_thread(self, func, output_func, **kwargs):
        self.new_thread = Thread(
            target=func,
            kwargs=dict(thread_queue=self.thread_queue, **kwargs)
        )
        self.new_thread.start()
        self.after(100, self.listen_for_result, output_func)

    def configure_gui(self):
        self.master.title("Comic Downloader")
        # self.master.geometry("1000x1000")

    def create_variables(self):
        self.selected_comic = tk.IntVar(self.master)
        self.selected_comic_name = tk.StringVar(self.master)
        self.selected_chapter = tk.IntVar(self.master)
        self.selected_chapter_name = tk.StringVar(self.master)
        self.loading_search_text = tk.StringVar(self.master)
        self.loading_chapter_text = tk.StringVar(self.master)
        self.download_chapters_text = tk.StringVar(self.master)
        self.search_results = []
        self.chapter_results = []

    def create_widgets(self):
        self.create_search()
        self.create_chapters()
        self.progress = ttk.Progressbar(
            self.master,
            mode = "indeterminate",
            length=350,
            orient='horizontal',
        )

    def place_widgets(self):
        self.progress.grid(row=0, column=0, columnspan=2,padx=10, pady=10)

        # search for comics
        self.search_input.grid(row=10, column=0, padx=10, pady=10, columnspan=2)
        self.search_btn.grid(row=20, column=0, padx=10, pady=10, columnspan=2)
        self.loading_search_label.grid(row=30, column=0, padx=10, pady=10, columnspan=2)
        self.search_result_box.grid(row=40, column=0, padx=10, pady=10, columnspan=2)

        # select chapters to download
        self.get_chapters_btn.grid(
            row=50, column=0, columnspan=2,padx=10, pady=10,)
        self.loading_chapter_results.grid(
            row=60, column=0, columnspan=2,padx=10, pady=10,)
        self.chapter_results_frame.grid(
            row=70, column=0, columnspan=2,padx=10, pady=10,)
        self.select_all_btn.grid(row=80, column=0)
        self.unselect_all_btn.grid(row=80, column=1)
        self.chapters_download_btn.grid(row=90, column=0, columnspan=2,padx=10, pady=10,)
        self.download_chapters_label.grid(row=100, column=0, columnspan=2,padx=10, pady=10,)


    def create_search(self):
        self.search_input = tk.Text(self.master, height=1, width=45)
        self.search_input.bind('<Return>', self.perform_search)

        self.search_btn = tk.Button(
            self.master, 
            text="Search for comics", 
            command=self.perform_search, 
            width=50
        )
        self.search_result_box = ttk.Combobox(
            self.master, 
            values=self.search_results,
            textvariable=self.selected_comic_name, 
            width=55
        )
        self.loading_search_label = tk.Label(
            self.master, textvariable=self.loading_search_text)

    def create_chapters(self):
        self.chapter_results_frame = ChaptersFrame(self.master)

        self.get_chapters_btn = tk.Button(
            self.master,
            text="Get Chapters",
            command=self.get_chapters,
            width=50,
            state="disabled"
        )
        self.chapters_download_btn = tk.Button(
            self.master,
            text="Download Chapters",
            command=self.download_chapters,
            width=50,
            state="disabled"
        )
        self.download_chapters_label = tk.Label(
            self.master, 
            textvariable=self.download_chapters_text
        )
        self.loading_chapter_results = tk.Label(
            self.master, 
            textvariable=self.loading_chapter_text
        )
        self.select_all_btn = tk.Button(
            self.master, 
            text="Select All", 
            command=self.set_all_chapters_selected, 
            width=25
        )
        self.unselect_all_btn = tk.Button(
            self.master, 
            text="Unselect All", 
            command=self.set_all_chapters_unselected, 
            width=25
        )
        

    def set_all_chapters_unselected(self):
        self.chapter_results_frame.chapter_listbox.selection_clear(0, tk.END)

    def set_all_chapters_selected(self):
        self.chapter_results_frame.chapter_listbox.select_set(0, tk.END)

    def get_selected_comic(self):
        comic = list(filter(
            lambda result: result['title'] == self.selected_comic_name.get(), self.search_results))
        if len(comic) == 1:
            return comic[0]

    def perform_search(self, event=None):
        self.progress.start()

        if len(self.search_results):
            self.search_results = []

        self.loading_search_text.set("Loading search results...")
        self.get_chapters_btn['state'] = "disable"
        search = self.search_input.get("1.0", tk.END).strip('\n')
        self.run_in_new_thread(self.ctrl.search_comics, self.complete_search, search_input=search)
        self.search_input.delete('1.0', tk.END)

    def complete_search(self, results):
        self.progress.stop()

        if len(results):
            self.search_results = results
            self.search_result_box['values'] = [r['title'] for r in results]
            self.selected_comic_name.set(results[0]['title'])
            self.selected_comic.set(0)
            self.get_chapters_btn['state'] = "normal"
            self.loading_search_text.set(
                f"Found {len(results)} comic{'' if len(results) == 1 else 's'}")
        else:
            self.loading_search_text.set(
                f"No results found, try a different search")

    def get_chapters(self):
        self.progress.start()

        self.loading_chapter_text.set("Loading chapters...")
        self.chapters_download_btn['state'] = "disabled"
        comic = self.get_selected_comic()
        self.run_in_new_thread(self.ctrl.get_chapters,
                               self.complete_get_chapters, comic=comic)

    def complete_get_chapters(self, results):
        self.progress.stop()

        if len(results):
            self.chapter_results = results
            self.chapter_results_frame.create_options(results)
            self.chapters_download_btn['state'] = "normal"
            self.loading_chapter_text.set(
                f"Found {len(results)} chapter{'' if len(results) == 1 else 's'}")
        else:
            self.loading_chapter_text.set(
                f"No chapters found, try a different comic")

    def download_chapters(self):
        self.progress.start()
        chapters = self.chapter_results_frame.get_selected_options()
        selected_chapters = list(
            filter(lambda chapter: chapter['title'] in chapters, self.chapter_results))
        self.run_in_new_thread(self.ctrl.download_chapters, self.complete_download,
                               comic=self.get_selected_comic(), chapters=selected_chapters)
        self.download_chapters_text.set(f"Downloading {len(selected_chapters)} chapter{'' if len(selected_chapters) == 1 else 's'}")
        self.search_btn['state'] = "disabled"
        self.get_chapters_btn['state'] = "disabled"
        self.chapters_download_btn['state'] = "disabled"

    def complete_download(self, results):
        self.progress.stop()
        if results:
            bad_chapters = "\n".join(results)
            error_text = f"Unable to download {len(results)} chapter{'s' if len(results) != 1 else ''}\n{bad_chapters}"
            self.download_chapters_text.set(error_text)
        else:
            self.download_chapters_text.set(f"Finished Downloading")
        self.search_btn['state'] = "normal"
        self.get_chapters_btn['state'] = "normal"
        self.chapters_download_btn['state'] = "normal"


if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()

'''
TODO:
add labels for indicating when data is loading / additional threads are running
add labels for information on data sizes and number of selected items
add buttons for selecting/deselecting all items

'''
