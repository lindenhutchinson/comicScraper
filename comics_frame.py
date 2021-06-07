# import tkinter as tk
# from tkinter import ttk


# class ComicsFrame(ttk.Frame):
#     def __init__(self, container, parent, *args, **kwargs):
#         super().__init__(container, *args, **kwargs)
#         self.parent = parent
#         self.create_scrollable()
#         self.create_variables()

#     def create_scrollable(self):
#         canvas = tk.Canvas(self, bg="white")
#         scrollbar = ttk.Scrollbar(
#             self, orient="vertical", command=canvas.yview)
#         self.scrollable_frame = ttk.Frame(canvas)

#         self.scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(
#                 scrollregion=canvas.bbox("all")
#             )
#         )
#         canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

#         canvas.configure(yscrollcommand=scrollbar.set)

#         canvas.grid(row=10, column=10)
#         scrollbar.grid(row=10, column=10, sticky="NSE")

#     def create_variables(self):
#         self.options = []
#         self.selected_option = tk.IntVar(value=-1)

#     def remove_options(self):
#         for btn in self.options:
#             btn.grid_forget()

#     def create_options(self, results):
#         if(len(self.options) > 0):
#             self.remove_options()
#             self.options = []
#             self.options_container.grid_forget()

#         self.options_container = tk.Frame(self.scrollable_frame, bg="white")
#         self.options_container.grid(sticky="N")

#         for res in results:
#             btn = tk.Radiobutton(
#                 self.options_container, 
#                 command=self.set_selected_option,
#                 text=res['title'],
#                 variable=self.selected_option, 
#                 value=results.index(res), 
#                 activebackground="lightgrey", 
#                 bg="white"
#             )
#             self.options.append(btn)
#             btn.grid(sticky="w")

#     def set_selected_option(self):
#         self.parent.selected_comic.set(self.selected_option.get())
#         self.parent.selected_comic_name.set(self.parent.search_results[self.selected_option.get()]['title'])
#         # return self.selected_option.get()
