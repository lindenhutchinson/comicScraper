import tkinter as tk
from chapter_controller import ChapterController
from constants import END
from scrollable_frame import ScrollableFrame



class MainApplication(tk.Frame):
    def __init__(self, master):
        self.controller = ChapterController('comics')
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_variables()
        self.create_widgets()
        

    def create_variables(self):
        self.selected_comic = tk.StringVar(self.master, value=-1)
        self.comic_options = []


    def perform_search(self):
        search = self.search_input.get("1.0", END).strip('\n')
        options, results = self.controller.search_comics(search)
        self.search_results.create_options(results)

    def create_search(self):
        self.search_input = tk.Text(self.master, height=1, width=40)
        self.search_btn = tk.Button(self.master, text="Search", command=self.perform_search, width=40)
        self.search_input.grid(row=0, column=10, padx=10,pady=10)
        self.search_btn.grid(row=10, column=10, padx=10,pady=10)

    def configure_gui(self):
        self.master.title("Comic Downloader")
        self.master.geometry("1000x1000")

    def create_widgets(self):
        self.create_search()
        self.search_results = ScrollableFrame(self.master)
        self.search_results.grid(row=20,column=10, padx=10)


if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()
