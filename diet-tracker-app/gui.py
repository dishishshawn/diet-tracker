import tkinter as tk
from tkinter import ttk
from database import get_session
from models import Meal, Workout
from datetime import date

class TrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Diet and Workout Tracker')
        self.initUI()

    def initUI(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        # Meal Form
        meal_frame = ttk.LabelFrame(main_frame, text='Log Meal')
        meal_frame.pack(fill='x', expand=True, pady=10)

        self.meal_date = ttk.Entry(meal_frame)
        self.meal_date.insert(0, date.today().isoformat())
        self.meal_desc = ttk.Entry(meal_frame)
        self.meal_calories = ttk.Entry(meal_frame)

        ttk.Label(meal_frame, text='Date:').grid(row=0, column=0, sticky='w')
        self.meal_date.grid(row=0, column=1, sticky='ew')
        ttk.Label(meal_frame, text='Meal Description:').grid(row=1, column=0, sticky='w')
        self.meal_desc.grid(row=1, column=1, sticky='ew')
        ttk.Label(meal_frame, text='Calories:').grid(row=2, column=0, sticky='w')
        self.meal_calories.grid(row=2, column=1, sticky='ew')

        self.log_meal_button = ttk.Button(meal_frame, text='Log Meal', command=self.log_meal)
        self.log_meal_button.grid(row=3, columnspan=2, pady=5)

        # Workout Form
        workout_frame = ttk.LabelFrame(main_frame, text='Log Workout')
        workout_frame.pack(fill='x', expand=True, pady=10)

        self.workout_date = ttk.Entry(workout_frame)
        self.workout_date.insert(0, date.today().isoformat())
        self.workout_desc = ttk.Entry(workout_frame)
        self.workout_duration = ttk.Entry(workout_frame)
        self.workout_calories = ttk.Entry(workout_frame)

        ttk.Label(workout_frame, text='Date:').grid(row=0, column=0, sticky='w')
        self.workout_date.grid(row=0, column=1, sticky='ew')
        ttk.Label(workout_frame, text='Workout Description:').grid(row=1, column=0, sticky='w')
        self.workout_desc.grid(row=1, column=1, sticky='ew')
        ttk.Label(workout_frame, text='Duration (min):').grid(row=2, column=0, sticky='w')
        self.workout_duration.grid(row=2, column=1, sticky='ew')
        ttk.Label(workout_frame, text='Calories Burned:').grid(row=3, column=0, sticky='w')
        self.workout_calories.grid(row=3, column=1, sticky='ew')

        self.log_workout_button = ttk.Button(workout_frame, text='Log Workout', command=self.log_workout)
        self.log_workout_button.grid(row=4, columnspan=2, pady=5)

    def log_meal(self):
        session = get_session()
        new_meal = Meal(
            date=date.fromisoformat(self.meal_date.get()),
            description=self.meal_desc.get(),
            calories=float(self.meal_calories.get())
        )
        session.add(new_meal)
        session.commit()
        session.close()
        self.meal_desc.delete(0, tk.END)
        self.meal_calories.delete(0, tk.END)

    def log_workout(self):
        session = get_session()
        new_workout = Workout(
            date=date.fromisoformat(self.workout_date.get()),
            description=self.workout_desc.get(),
            duration=float(self.workout_duration.get()),
            calories_burned=float(self.workout_calories.get())
        )
        session.add(new_workout)
        session.commit()
        session.close()
        self.workout_desc.delete(0, tk.END)
        self.workout_duration.delete(0, tk.END)
        self.workout_calories.delete(0, tk.END)
