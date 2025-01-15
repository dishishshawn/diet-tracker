import tkinter as tk
from tkinter import ttk
from database import get_session
from models import Meal, Workout
from datetime import date, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Diet and Workout Tracker')
        self.initUI()

    def initUI(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Meal Form
        meal_frame = ttk.LabelFrame(main_frame, text='Log Meal')
        meal_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

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

        # Meals List
        self.meals_list = tk.Listbox(main_frame)
        self.meals_list.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.update_meals_list()

        self.edit_meal_button = ttk.Button(main_frame, text='Edit Meal', command=self.edit_meal)
        self.edit_meal_button.grid(row=0, column=2, padx=5, pady=5)

        self.remove_meal_button = ttk.Button(main_frame, text='Remove Meal', command=self.remove_meal)
        self.remove_meal_button.grid(row=0, column=3, padx=5, pady=5)

        # Workout Form
        workout_frame = ttk.LabelFrame(main_frame, text='Log Workout')
        workout_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

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

        # Workouts List
        self.workouts_list = tk.Listbox(main_frame)
        self.workouts_list.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        self.update_workouts_list()

        self.edit_workout_button = ttk.Button(main_frame, text='Edit Workout', command=self.edit_workout)
        self.edit_workout_button.grid(row=1, column=2, padx=5, pady=5)

        self.remove_workout_button = ttk.Button(main_frame, text='Remove Workout', command=self.remove_workout)
        self.remove_workout_button.grid(row=1, column=3, padx=5, pady=5)

        # Calories Graph
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, main_frame)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.update_calories_graph()

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

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
        self.update_meals_list()
        self.update_calories_graph()

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
        self.update_workouts_list()
        self.update_calories_graph()

    def update_meals_list(self):
        self.meals_list.delete(0, tk.END)
        session = get_session()
        today_meals = session.query(Meal).filter(Meal.date == date.today()).all()
        for meal in today_meals:
            self.meals_list.insert(tk.END, f"{meal.description}: {meal.calories} calories")
        session.close()

    def update_workouts_list(self):
        self.workouts_list.delete(0, tk.END)
        session = get_session()
        past_workouts = session.query(Workout).order_by(Workout.date.desc()).all()
        for workout in past_workouts:
            self.workouts_list.insert(tk.END, f"{workout.date} - {workout.description}: {workout.calories_burned} calories burned")
        session.close()

    def update_calories_graph(self):
        session = get_session()
        meals = session.query(Meal).all()
        workouts = session.query(Workout).all()
        session.close()

        if not meals and not workouts:
            return

        start_date = min(min(meal.date for meal in meals), min(workout.date for workout in workouts))
        end_date = max(max(meal.date for meal in meals), max(workout.date for workout in workouts))
        dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        net_calories = []
        for d in dates:
            total_meal_calories = sum(meal.calories for meal in meals if meal.date == d)
            total_workout_calories = sum(workout.calories_burned for workout in workouts if workout.date == d)
            net_calories.append(total_meal_calories - total_workout_calories)

        self.ax.clear()
        self.ax.plot(dates, net_calories, marker='o')
        self.ax.set_title('Net Calories Per Day')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Net Calories')
        self.canvas.draw()

    def edit_meal(self):
        selected_index = self.meals_list.curselection()
        if not selected_index:
            return
        selected_meal = self.meals_list.get(selected_index)
        meal_desc, meal_calories = selected_meal.split(': ')
        meal_calories = meal_calories.split(' ')[0]

        self.meal_desc.delete(0, tk.END)
        self.meal_desc.insert(0, meal_desc)
        self.meal_calories.delete(0, tk.END)
        self.meal_calories.insert(0, meal_calories)

        self.remove_meal()

    def remove_meal(self):
        selected_index = self.meals_list.curselection()
        if not selected_index:
            return
        selected_meal = self.meals_list.get(selected_index)
        meal_desc, meal_calories = selected_meal.split(': ')
        meal_calories = meal_calories.split(' ')[0]

        session = get_session()
        meal = session.query(Meal).filter(Meal.description == meal_desc, Meal.calories == meal_calories).first()
        if meal:
            session.delete(meal)
            session.commit()
        session.close()
        self.update_meals_list()
        self.update_calories_graph()

    def edit_workout(self):
        selected_index = self.workouts_list.curselection()
        if not selected_index:
            return
        selected_workout = self.workouts_list.get(selected_index)
        workout_date, workout_desc, workout_calories = selected_workout.split(' - ')[1].split(': ')
        workout_calories = workout_calories.split(' ')[0]

        self.workout_desc.delete(0, tk.END)
        self.workout_desc.insert(0, workout_desc)
        self.workout_calories.delete(0, tk.END)
        self.workout_calories.insert(0, workout_calories)

        self.remove_workout()

    def remove_workout(self):
        selected_index = self.workouts_list.curselection()
        if not selected_index:
            return
        selected_workout = self.workouts_list.get(selected_index)
        workout_date, workout_desc, workout_calories = selected_workout.split(' - ')[1].split(': ')
        workout_calories = workout_calories.split(' ')[0]

        session = get_session()
        workout = session.query(Workout).filter(Workout.description == workout_desc, Workout.calories_burned == workout_calories).first()
        if workout:
            session.delete(workout)
            session.commit()
        session.close()
        self.update_workouts_list()
        self.update_calories_graph()
