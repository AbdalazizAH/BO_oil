import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from matplotlib.figure import Figure


class OilProperties:
    @staticmethod
    def Rs_glaso(pres, temp, API, gas_sg):
        a = -0.30218
        b = 1.7447
        c = 1.7669 - np.log10(pres)
        chi = 10 ** ((-b + np.sqrt(b**2 - 4 * a * c)) / (2 * a))
        return (chi * API**0.989 / temp**0.172) ** (1 / 0.816) * gas_sg

    @staticmethod
    def oil_fvf_glaso(temp, Rs, oil_sg, gas_sg):
        y = Rs * (gas_sg / oil_sg) ** 0.526 + 0.968 * temp
        logbo_1 = -6.58511 + 2.91329 * np.log10(y) - 0.27683 * np.log10(y) ** 2
        bo_1 = 10**logbo_1
        return bo_1 + 1

    @staticmethod
    def oil_Rs_standing(pres, temp, API, gas_sg):
        return (
            (pres / 18.2 + 1.4) * 10 ** (0.0125 * API) / 10 ** (0.00091 * temp)
        ) ** (1 / 0.83) * gas_sg

    @staticmethod
    def oil_fvf_standing(temp, Rs, oil_sg, gas_sg):
        return 0.972 + 1.47e-4 * (Rs * (gas_sg / oil_sg) ** 0.5 + 1.25 * temp) ** 1.175


class CustomButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.configure(
            bg="#4a4a4a",
            fg="white",
            activebackground="#666666",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            font=("Helvetica", 10, "bold"),
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["bg"] = "#666666"

    def on_leave(self, e):
        self["bg"] = "#4a4a4a"


class OilFVFCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Oil Formation Volume Factor Calculator")
        master.geometry("1500x800")  # Increased width to accommodate the new frame
        master.configure(bg="#2c2c2c")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2c2c2c")
        self.style.configure(
            "TLabel", background="#2c2c2c", foreground="white", font=("Helvetica", 10)
        )
        self.style.configure(
            "TEntry", fieldbackground="#3c3c3c", foreground="white", insertcolor="white"
        )
        self.style.map("TCombobox", fieldbackground=[("readonly", "#3c3c3c")])
        self.style.map("TCombobox", selectbackground=[("readonly", "#3c3c3c")])
        self.style.map("TCombobox", selectforeground=[("readonly", "white")])

        # Configure Treeview colors
        self.style.configure(
            "Treeview",
            background="#3c3c3c",
            foreground="white",
            fieldbackground="#3c3c3c",
        )
        self.style.map("Treeview", background=[("selected", "#4c4c4c")])

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.input_frame = ttk.Frame(self.main_frame, padding="10")
        self.input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.csv_display_frame = ttk.Frame(self.main_frame, padding="5")
        self.csv_display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_input_fields()
        self.create_buttons()
        self.create_csv_display()

        self.result_label = ttk.Label(
            self.input_frame, text="", font=("Helvetica", 10, "bold")
        )
        self.result_label.pack(pady=10)

    def create_input_fields(self):
        fields = [
            ("Bubble Point Pressure (psia):", "pb_entry", "5868"),
            ("Max Pressure (psia):", "max_pressure_entry", "6899"),
            ("API Gravity:", "api_entry", "42.002"),
            ("Gas Specific Gravity:", "gas_sg_entry", "0.709"),
            ("Temperature (°F):", "temp_entry", "292.1"),
        ]

        for label, attr, default in fields:
            frame = ttk.Frame(self.input_frame)
            frame.pack(fill=tk.X, pady=5)
            ttk.Label(frame, text=label, width=25).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=15)
            entry.pack(side=tk.RIGHT)
            entry.insert(0, default)
            setattr(self, attr, entry)

        self.equation_bo = tk.StringVar(value="Glaso")
        self.equation_rs = tk.StringVar(value="Glaso")

        frame = ttk.Frame(self.input_frame)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text="Select Bo Equation:", width=25).pack(side=tk.LEFT)
        ttk.Combobox(
            frame,
            textvariable=self.equation_bo,
            values=("Glaso", "Standing"),
            width=13,
            state="readonly",
        ).pack(side=tk.RIGHT)

        frame = ttk.Frame(self.input_frame)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text="Select Rs Equation:", width=25).pack(side=tk.LEFT)
        ttk.Combobox(
            frame,
            textvariable=self.equation_rs,
            values=("Glaso", "Standing"),
            width=13,
            state="readonly",
        ).pack(side=tk.RIGHT)

        # CSV column name inputs
        self.pressure_column = tk.StringVar(value="Pressure")
        self.fvf_column = tk.StringVar(value="FVF")

        frame = ttk.Frame(self.input_frame)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text="CSV Pressure Column:", width=25).pack(side=tk.LEFT)
        ttk.Entry(frame, textvariable=self.pressure_column, width=15).pack(
            side=tk.RIGHT
        )

        frame = ttk.Frame(self.input_frame)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text="CSV FVF Column:", width=25).pack(side=tk.LEFT)
        ttk.Entry(frame, textvariable=self.fvf_column, width=15).pack(side=tk.RIGHT)

    def create_buttons(self):
        CustomButton(
            self.input_frame, text="Generate Plot", command=self.generate_plot
        ).pack(fill=tk.X, pady=10)
        CustomButton(
            self.input_frame, text="Load CSV Data", command=self.load_csv
        ).pack(fill=tk.X, pady=10)

    def create_csv_display(self):
        ttk.Label(
            self.csv_display_frame, text="CSV Data", font=("Helvetica", 12, "bold")
        ).pack(pady=(0, 10))

        # Create Treeview widget
        self.tree = ttk.Treeview(self.csv_display_frame, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(
            self.csv_display_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.csv_data = pd.read_csv(file_path)
                pressure_col = self.pressure_column.get()
                fvf_col = self.fvf_column.get()

                if (
                    pressure_col not in self.csv_data.columns
                    or fvf_col not in self.csv_data.columns
                ):
                    raise ValueError(
                        f"Columns '{pressure_col}' and '{fvf_col}' must be present in the CSV file."
                    )

                self.display_csv_data()
                messagebox.showinfo("Success", "CSV file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file: {str(e)}")

    def display_csv_data(self):
        # Clear existing data
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Configure columns
        self.tree["columns"] = list(self.csv_data.columns)
        for col in self.csv_data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)

        # Add data to the treeview
        for i, row in self.csv_data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def generate_plot(self):
        Pb = float(self.pb_entry.get())
        max_pressure = float(self.max_pressure_entry.get())
        API = float(self.api_entry.get())
        gas_sg = float(self.gas_sg_entry.get())
        temp = float(self.temp_entry.get())
        oil_sg = 141.5 / (API + 131.5)

        pressures = np.linspace(max_pressure, 0, 1000)
        Rs_values = []
        fvf_values = []

        Rs_func = (
            OilProperties.Rs_glaso
            if self.equation_rs.get() == "Glaso"
            else OilProperties.oil_Rs_standing
        )
        fvf_func = (
            OilProperties.oil_fvf_glaso
            if self.equation_bo.get() == "Glaso"
            else OilProperties.oil_fvf_standing
        )

        for p in pressures:
            if p >= Pb:
                Rs = Rs_func(Pb, temp, API, gas_sg)
                Bo_pb = fvf_func(temp, Rs, oil_sg, gas_sg)
                co = 1.5e-5
                Bo = Bo_pb * np.exp(-co * (p - Pb))
            else:
                Rs = Rs_func(p, temp, API, gas_sg)
                Bo = fvf_func(temp, Rs, oil_sg, gas_sg)

            Rs_values.append(Rs)
            fvf_values.append(Bo)

        self.plot_results(pressures, fvf_values, Pb)

    def plot_results(self, pressures, fvf_values, Pb):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(8, 6), dpi=100)
        fig.patch.set_facecolor("#2c2c2c")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#2c2c2c")

        ax.plot(pressures, fvf_values, "b-", label="Calculated FVF")

        if hasattr(self, "csv_data"):
            pressure_col = self.pressure_column.get()
            fvf_col = self.fvf_column.get()
            ax.scatter(
                self.csv_data[pressure_col],
                self.csv_data[fvf_col],
                color="red",
                marker="*",
                label="CSV Data",
            )

        ax.set_title("Formation Volume Factor vs Pressure", color="white", fontsize=14)
        ax.set_xlabel("Pressure (psia)", color="white")
        ax.set_ylabel("Formation Volume Factor (bbl/STB)", color="white")
        ax.tick_params(colors="white")
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.set_xlim(max(pressures), 0)
        ax.invert_xaxis()

        for spine in ax.spines.values():
            spine.set_edgecolor("white")

        bubble_point_fvf = fvf_values[np.argmin(np.abs(pressures - Pb))]
        ax.plot(Pb, bubble_point_fvf, "go", label="Bubble Point")
        ax.legend(facecolor="#2c2c2c", edgecolor="white", labelcolor="white")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.result_label.config(
            text=f"Bubble Point Pressure: {Pb:.2f} psia\nFVF at Bubble Point: {bubble_point_fvf:.4f} bbl/STB"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = OilFVFCalculator(root)
    root.mainloop()
