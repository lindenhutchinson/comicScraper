import tkinter as tk
from tkinter import ttk
from constants import END
class ChaptersFrame(ttk.Frame):
    def __init__(self, container, parent, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.parent = parent
        self.options = []
        self.selected_option = tk.IntVar(value=0)

        self.chapter_listbox = tk.Listbox(self,selectmode = "multiple", bg="white", width=60)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.chapter_listbox.yview)
        # self.scrollable_frame = ttk.Frame(self)

        # self.scrollable_frame.bind(
        #     "<Configure>",
        #     lambda e: self.chapter_listbox.configure(
        #         scrollregion=self.chapter_listbox.bbox("all")
        #     )
        # )
        # canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.chapter_listbox.configure(yscrollcommand=scrollbar.set)

        # canvas.grid(row=10, column=10)
        scrollbar.grid(row=10, column=10, sticky="NSE")
        self.chapter_listbox.grid(row=10, column=10)



    def create_options(self, results):
        if self.chapter_listbox.size():
            self.chapter_listbox.delete(0, END)
        for res in results:
            self.chapter_listbox.insert(0, res['title']) # insert from the start of the array to reverse the dictionary data order - it is stored backwards in the scraped data

    def get_selected_options(self):
        selected = []
        for i in self.chapter_listbox.curselection():
            selected.append(self.chapter_listbox.get(i))

        return selected
        # self.parent.selected_chapter.set(self.selected_option.get())
        # self.parent.selected_chapter.set(self.parent.chapter_results[self.selected_option.get()]['title'])
