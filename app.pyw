# Written mostly by ChatGPT
# Supervised by Nick Pasta with some small changes

import tkinter as tk
from tkinter import ttk, filedialog
import csv
import json
from datetime import datetime
from collections import Counter

class DropLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MMO Drop Logger")
        self.root.attributes('-topmost', 1)

        self.data = []
        self.drop_counter = Counter()

        # Dropdown data sources
        self.player_classes = set()
        self.enemy_names = set()
        self.item_drops = set()
        self.item_rarities = set()

        # Ask for player attribution
        self.player_attribution = tk.simpledialog.askstring("Player Attribution", "Enter your player name:")

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Player Class
        ttk.Label(frame, text="Player Class:").grid(row=0, column=0, padx=5, pady=5)
        self.player_class_var = tk.StringVar()
        self.player_class_combobox = ttk.Combobox(frame, textvariable=self.player_class_var, values=sorted(self.player_classes))
        self.player_class_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Enemy Name
        ttk.Label(frame, text="Enemy Name:").grid(row=1, column=0, padx=5, pady=5)
        self.enemy_name_var = tk.StringVar()
        self.enemy_name_combobox = ttk.Combobox(frame, textvariable=self.enemy_name_var, values=sorted(self.enemy_names))
        self.enemy_name_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.enemy_name_combobox.bind("<<ComboboxSelected>>", self.update_default_item_drop)

        # Enemy Level
        ttk.Label(frame, text="Enemy Level:").grid(row=2, column=0, padx=5, pady=5)
        self.enemy_level_var = tk.StringVar()
        self.enemy_level_entry = ttk.Entry(frame, textvariable=self.enemy_level_var)
        self.enemy_level_entry.grid(row=2, column=1, padx=5, pady=5)

        # Item Drop
        ttk.Label(frame, text="Item Drop:").grid(row=3, column=0, padx=5, pady=5)
        self.item_drop_var = tk.StringVar()
        self.item_drop_combobox = ttk.Combobox(frame, textvariable=self.item_drop_var, values=sorted(self.item_drops))
        self.item_drop_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Item Rarity
        ttk.Label(frame, text="Item Rarity:").grid(row=4, column=0, padx=5, pady=5)
        self.item_rarity_var = tk.StringVar()
        self.item_rarity_combobox = ttk.Combobox(frame, textvariable=self.item_rarity_var, values=sorted(self.item_rarities))
        self.item_rarity_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Weapon Untuned
        ttk.Label(frame, text="Weapon Untuned:").grid(row=5, column=0, padx=5, pady=5)
        self.untuned_var = tk.BooleanVar()
        self.untuned_checkbox = ttk.Checkbutton(frame, variable=self.untuned_var)
        self.untuned_checkbox.grid(row=5, column=1, padx=5, pady=5)

        # Buttons
        self.log_button = ttk.Button(frame, text="Log Drop", command=self.log_drop)
        self.log_button.grid(row=6, column=0, padx=5, pady=5)

        self.export_button = ttk.Button(frame, text="Export Data", command=self.export_data)
        self.export_button.grid(row=6, column=1, padx=5, pady=5)

        self.load_button = ttk.Button(frame, text="Load Data", command=self.load_data)
        self.load_button.grid(row=7, column=0, padx=5, pady=5)

        # Total Logs Counter
        self.log_count_var = tk.StringVar(value="Total Logs: 0")
        self.log_count_label = ttk.Label(frame, textvariable=self.log_count_var)
        self.log_count_label.grid(row=7, column=1, padx=5, pady=5)

        # Data Display
        self.tree = ttk.Treeview(self.root, columns=("Time", "Player Attribution", "Player Class", "Enemy Name", "Enemy Level", "Item Drop", "Item Rarity", "Untuned"), show="headings")
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(padx=10, pady=10)

    def log_drop(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        player_class = self.player_class_var.get()
        enemy_name = self.enemy_name_var.get()
        enemy_level = self.enemy_level_var.get()
        item_drop = self.item_drop_var.get()
        item_rarity = self.item_rarity_var.get()
        untuned = self.untuned_var.get()

        # Append data
        entry = (current_time, self.player_attribution, player_class, enemy_name, enemy_level, item_drop, item_rarity, untuned)
        self.data.append(entry)
        self.drop_counter[(enemy_name, item_drop)] += 1

        # Save data to file
        self.save_data()

        # Update dropdown options
        if player_class and player_class not in self.player_classes:
            self.player_classes.add(player_class)
            self.player_class_combobox["values"] = sorted(self.player_classes)

        if enemy_name and enemy_name not in self.enemy_names:
            self.enemy_names.add(enemy_name)
            self.enemy_name_combobox["values"] = sorted(self.enemy_names)

        if item_drop and item_drop not in self.item_drops:
            self.item_drops.add(item_drop)
            self.item_drop_combobox["values"] = sorted(self.item_drops)

        if item_rarity and item_rarity not in self.item_rarities:
            self.item_rarities.add(item_rarity)
            self.item_rarity_combobox["values"] = sorted(self.item_rarities)

        # Update tree view
        self.tree.insert("", "end", values=entry)

        # Scroll to the bottom
        self.tree.yview_moveto(1.0)

        # Reset specific fields
        self.update_default_item_drop(entry)
        self.item_rarity_var.set("None")
        self.untuned_var.set(False)

        # Update log count
        self.log_count_var.set(f"Total Logs: {len(self.data)}")

    def export_data(self):
        filetypes = [("CSV files", "*.csv"), ("JSON files", "*.json")]
        file_path = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes)

        if file_path:
            if file_path.endswith(".csv"):
                self.export_to_csv(file_path)
            elif file_path.endswith(".json"):
                self.export_to_json(file_path)

    def export_to_csv(self, file_path):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "Player Attribution", "Player Class", "Enemy Name", "Enemy Level", "Item Drop", "Item Rarity", "Untuned"])
            writer.writerows(self.data)

    def export_to_json(self, file_path):
        with open(file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def load_data(self):
        filetypes = [("CSV files", "*.csv"), ("JSON files", "*.json")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:
            self.data.clear()
            self.drop_counter.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)

            if file_path.endswith(".csv"):
                self.load_from_csv(file_path)
            elif file_path.endswith(".json"):
                self.load_from_json(file_path)

    def load_from_csv(self, file_path):
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                self.data.append(tuple(row))
                self.tree.insert("", "end", values=row)
                self.update_dropdowns_from_entry(row)
                self.drop_counter[(row[3], row[5])] += 1
        self.log_count_var.set(f"Total Logs: {len(self.data)}")

    def load_from_json(self, file_path):
        with open(file_path, "r") as file:
            loaded_data = json.load(file)
            for entry in loaded_data:
                self.data.append(tuple(entry))
                self.tree.insert("", "end", values=entry)
                self.update_dropdowns_from_entry(entry)
                self.drop_counter[(entry[3], entry[5])] += 1
        self.log_count_var.set(f"Total Logs: {len(self.data)}")

    def update_dropdowns_from_entry(self, entry):
        _, _, player_class, enemy_name, _, item_drop, item_rarity, _ = entry

        if player_class and player_class not in self.player_classes:
            self.player_classes.add(player_class)
            self.player_class_combobox["values"] = sorted(self.player_classes)

        if enemy_name and enemy_name not in self.enemy_names:
            self.enemy_names.add(enemy_name)
            self.enemy_name_combobox["values"] = sorted(self.enemy_names)

        if item_drop and item_drop not in self.item_drops:
            self.item_drops.add(item_drop)
            self.item_drop_combobox["values"] = sorted(self.item_drops)

        if item_rarity and item_rarity not in self.item_rarities:
            self.item_rarities.add(item_rarity)
            self.item_rarity_combobox["values"] = sorted(self.item_rarities)

    def update_default_item_drop(self, event):
        selected_enemy = self.enemy_name_var.get()
        if selected_enemy:
            most_common_item = max((item for (enemy, item) in self.drop_counter.keys() if enemy == selected_enemy),
                                   key=lambda i: self.drop_counter[(selected_enemy, i)],
                                   default="None")
            self.item_drop_var.set(most_common_item)

    def save_data(self):
        with open("auto_saved_data.json", "w") as file:
            json.dump(self.data, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = DropLoggerApp(root)
    root.mainloop()
