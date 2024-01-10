import tkinter as tk


class Options(object):
    def __init__(self, root, plot_contour_values):
        self.root = root
        self.plot_contour_values = plot_contour_values

        self.plot_contour_values_btn = tk.Checkbutton(
            self.root,
            text="Показывать значения на контурах",
            variable=self.plot_contour_values
        )
        self.plot_contour_values_btn.grid(row=2, column=2)

  