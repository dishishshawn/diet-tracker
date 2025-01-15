import json
from datetime import datetime
import tkinter as tk
from gui import DietTrackerApp

class DietTracker:
    def __init__(self):
        self.meals = []

    def add_meal(self, meal, calories):
        self.meals.append({
            'meal': meal,
            'calories': calories,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def get_meals(self):
        return self.meals

    def save_meals(self, filename='meals.json'):
        with open(filename, 'w') as file:
            json.dump(self.meals, file)

    def load_meals(self, filename='meals.json'):
        try:
            with open(filename, 'r') as file:
                self.meals = json.load(file)
        except FileNotFoundError:
            self.meals = []

class WorkoutJournal:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout, duration):
        self.workouts.append({
            'workout': workout,
            'duration': duration,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def get_workouts(self):
        return self.workouts

    def save_workouts(self, filename='workouts.json'):
        with open(filename, 'w') as file:
            json.dump(self.workouts, file)

    def load_workouts(self, filename='workouts.json'):
        try:
            with open(filename, 'r') as file:
                self.workouts = json.load(file)
        except FileNotFoundError:
            self.workouts = []

if __name__ == "__main__":
    diet_tracker = DietTracker()
    workout_journal = WorkoutJournal()

    # Example usage
    diet_tracker.add_meal('Breakfast', 300)
    diet_tracker.save_meals()

    workout_journal.add_workout('Running', 30)
    workout_journal.save_workouts()

    print("Meals:", diet_tracker.get_meals())
    print("Workouts:", workout_journal.get_workouts())

    # Open GUI.py
    root = tk.Tk()
    app = DietTrackerApp(root)
    root.mainloop()