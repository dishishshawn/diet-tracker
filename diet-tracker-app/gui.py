import tkinter as tk
from tkinter import messagebox
from main import DietTracker

class DietTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diet Tracker")
        self.diet_tracker = DietTracker()
        self.diet_tracker.load_meals()

        self.label = tk.Label(root, text="Enter food item:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.calories_label = tk.Label(root, text="Enter calories:")
        self.calories_label.pack()

        self.calories_entry = tk.Entry(root)
        self.calories_entry.pack()

        self.add_button = tk.Button(root, text="Add Food", command=self.add_food)
        self.add_button.pack()

        self.show_button = tk.Button(root, text="Show Diet", command=self.show_diet)
        self.show_button.pack()

    def add_food(self):
        food_item = self.entry.get()
        calories = self.calories_entry.get()
        if food_item and calories:
            try:
                calories = int(calories)
                self.diet_tracker.add_meal(food_item, calories)
                self.diet_tracker.save_meals()
                messagebox.showinfo("Success", f"{food_item} added to your diet.")
                self.entry.delete(0, tk.END)
                self.calories_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid number for calories.")
        else:
            messagebox.showwarning("Input Error", "Please enter a food item and calories.")

    def show_diet(self):
        meals = self.diet_tracker.get_meals()
        diet_str = "\n".join([f"{meal['meal']} ({meal['calories']} calories)" for meal in meals])
        messagebox.showinfo("Your Diet", diet_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = DietTrackerApp(root)
    root.mainloop()