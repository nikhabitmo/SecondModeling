import math
import tkinter as tk
import numpy as np
import matplotlib as mpl
from matplotlib.figure import Figure
import matplotlib.backends.backend_tkagg as backend_tkagg
import faraday_numerics
import entry_boxes
import options


class FaradayCageApplication(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.wm_title("Клетка Фарадея")

        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=4, column=0, columnspan=5)

        self.fig = mpl.figure.Figure(figsize=(5, 4), dpi=125)

        self.sub_plt = self.fig.add_subplot(111)
        self.sub_plt.set_aspect('equal')

        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack()

        self.n, self.r, self.zs = [tk.IntVar(), tk.DoubleVar(), tk.DoubleVar()]
        [self.n.set(12), self.r.set(0.1), self.zs.set(2.0)]

        self.entry_boxes = entry_boxes.EntryBoxes(
            self.parent,
            self.n,
            self.r,
            self.zs
        )

        self.plot_contour_values = tk.BooleanVar()

        self.option_check_buttons = options.Options(
            self.parent,
            self.plot_contour_values,
        )

        self.plot_ptn_btn = tk.Button(
            self.parent,
            text="Запустить",
            command=lambda: self.calculate_to_plot(),
            width=10
        )
        self.plot_ptn_btn.grid(row=0, column=2)

    def calculate_to_plot(self):
        self.n_value, self.r_value, self.zs_value = [self.n.get(), self.r.get(), self.zs.get()]

        self.xx, self.yy, self.uu = faraday_numerics.run_simulation(
            self.n_value,
            self.r_value,
            self.zs_value
        )

        self.plot_potential()

    def plot_potential(self):
        self.clear_plot()

        wire_lst = range(1, self.n_value+1)

        unit_roots = np.array([math.e**(2j*math.pi*m/self.n_value) for m in wire_lst])
        self.sub_plt.scatter(unit_roots.real, unit_roots.imag, color='blue')

        self.sub_plt.plot(self.zs_value.real, self.zs_value.imag, '.r')

        levels = np.arange(-2, 2, 0.1)
        cont_plt = self.sub_plt.contour(
            self.xx,
            self.yy,
            self.uu,
            levels=levels,
            colors=('black'),
            corner_mask=True
        )

        if (self.plot_contour_values.get()):
            self.sub_plt.clabel(cont_plt, inline=1, fontsize=10)

        self.canvas.draw()

    def clear_plot(self):
        self.sub_plt.cla()
        self.canvas.draw()


def main():
    root = tk.Tk()
    FaradayCageApplication(root)
    tk.mainloop()


if __name__ == '__main__':
    main()
