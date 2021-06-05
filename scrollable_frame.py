import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.options = []
        self.selected_option = tk.StringVar(value=-1)
        canvas = tk.Canvas(self, bg="white")
        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=10, column=10)
        scrollbar.grid(row=10, column=10, sticky="NSE")

    def remove_options(self):
        for btn in self.options:
            btn.grid_forget()

    def create_options(self, results):
        if(len(self.options) > 0):
            self.remove_options()
            self.options = []
            self.options_container.grid_forget()

        self.options_container = tk.Frame(self.scrollable_frame, bg="white")
        self.options_container.grid(sticky="N")

        for res in results:
            btn = tk.Radiobutton(self.options_container, text=res['title'],
                                 variable=self.selected_option, value=res['url'], highlightbackground="yellow", activebackground="lightgrey", bg="white")
            self.options.append(btn)
            btn.grid(sticky="w")

    def get_selected_option(self):
        return self.selected_option.get()
