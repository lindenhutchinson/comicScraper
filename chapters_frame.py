import tkinter as tk
from tkinter import ttk

class ChaptersFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.options = []
        self.selected_option = tk.IntVar(value=0)

        self.chapter_listbox = tk.Listbox(self,selectmode = "multiple", bg="white", width=60)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.chapter_listbox.yview)

        self.chapter_listbox.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(row=10, column=10, sticky="NSE")
        self.chapter_listbox.grid(row=10, column=10)



    def create_options(self, results):
        if self.chapter_listbox.size():
            self.chapter_listbox.delete(0, tk.END)
        for res in results:
            self.chapter_listbox.insert(tk.END, res['title'])

    def get_selected_options(self):
        selected = []
        for i in self.chapter_listbox.curselection():
            selected.append(self.chapter_listbox.get(i))

        return selected
