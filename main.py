import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MoneyTracker(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Money Tracker")
        self.geometry("900x500")

        self.total_money = 1000
        self.used_money = 200

        self._build_ui()
        self._init_charts()

    def _build_ui(self):
        left = ctk.CTkFrame(self, width=200)
        left.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(left, text="Total Money").pack(pady=(10, 0))
        self.total_entry = ctk.CTkEntry(left)
        self.total_entry.insert(0, str(self.total_money))
        self.total_entry.pack(pady=5)

        ctk.CTkLabel(left, text="Used Money").pack(pady=(10, 0))
        self.used_entry = ctk.CTkEntry(left)
        self.used_entry.insert(0, str(self.used_money))
        self.used_entry.pack(pady=5)

        ctk.CTkButton(left, text="Update", command=self.update_charts).pack(pady=20)

        self.percent_label = ctk.CTkLabel(left, text="")
        self.percent_label.pack()

        self.right = ctk.CTkFrame(self)
        self.right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def _init_charts(self):
        self.fig, (self.ax_pie, self.ax_bar) = plt.subplots(1, 2, figsize=(7, 4))
        self.fig.tight_layout()

        remaining = self.total_money - self.used_money

        self.pie_wedges, _, self.pie_texts = self.ax_pie.pie(
            [self.used_money, remaining],
            labels=["Used", "Remaining"],
            autopct="%1.1f%%",
            colors=["#ff6b6b", "#4ecdc4"]
        )
        self.ax_pie.set_title("Money Usage")

    
        self.bar_container = self.ax_bar.bar(
            ["Used", "Remaining"],
            [self.used_money, remaining],
            color=["#ff6b6b", "#4ecdc4"]
        )
        self.ax_bar.set_ylim(0, self.total_money)
        self.ax_bar.set_title("Amount")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self._update_percent_label()

    def update_charts(self):
        try:
            self.total_money = float(self.total_entry.get())
            self.used_money = float(self.used_entry.get())
        except ValueError:
            return

        remaining = max(self.total_money - self.used_money, 0)

        values = [self.used_money, remaining]
        total = sum(values)

        angle = 0
        for wedge, value in zip(self.pie_wedges, values):
            theta1 = angle
            theta2 = angle + (value / total) * 360 if total else angle
            wedge.set_theta1(theta1)
            wedge.set_theta2(theta2)
            angle = theta2

    
        self.bar_container[0].set_height(self.used_money)
        self.bar_container[1].set_height(remaining)
        self.ax_bar.set_ylim(0, max(self.total_money, 1))

        self._update_percent_label()
        self.canvas.draw_idle()

    def _update_percent_label(self):
        percent = (self.used_money / self.total_money) * 100 if self.total_money else 0
        self.percent_label.configure(text=f"Used: {percent:.1f}%")

if __name__ == "__main__":
    app = MoneyTracker()
    app.mainloop()
