import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime, timedelta

# Define global variables
countdown_job = None
shutdown_start_time = None

def shutdown_at(hours, minutes, period):
    global shutdown_start_time, countdown_job
    try:
        current_time = datetime.now()
        
        # Convert the selected time to 24-hour format
        if period == "PM" and hours < 12:
            hours += 12
        elif period == "AM" and hours == 12:
            hours = 0

        shutdown_start_time = current_time.replace(hour=hours, minute=minutes, second=0, microsecond=0)

        # If the specified time is in the past, add 24 hours to it
        if shutdown_start_time < current_time:
            shutdown_start_time += timedelta(days=1)

        time_difference = shutdown_start_time - current_time
        seconds_until_shutdown = int(time_difference.total_seconds())

        os.system(f'shutdown /s /t {seconds_until_shutdown}')
        countdown_label.pack(side="bottom")
        countdown(seconds_until_shutdown)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid time.")

def shutdown_in_minutes(minutes):
    global shutdown_start_time, countdown_job
    try:
        current_time = datetime.now()
        shutdown_start_time = current_time + timedelta(minutes=minutes)
        time_difference = shutdown_start_time - current_time
        seconds_until_shutdown = int(time_difference.total_seconds())

        os.system(f'shutdown /s /t {seconds_until_shutdown}')
        countdown_label.pack(side="bottom")
        countdown(seconds_until_shutdown)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of minutes.")

def countdown(seconds):
    global countdown_job, shutdown_start_time
    remaining_time = shutdown_start_time - datetime.now()
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    countdown_label.config(text=f"Shutdown in: {hours:02d} hours {minutes:02d} minutes {seconds:02d} seconds")
    
    countdown_job = root.after(1000, countdown, seconds - 1) if seconds > 0 else None

def cancel_shutdown():
    global countdown_job, countdown_label
    root.after_cancel(countdown_job)  # Stop the countdown job
    countdown_label.pack_forget()  # Hide the countdown label
    os.system('shutdown /a')  # Cancel the shutdown command

# Create the main window
root = tk.Tk()
root.title("Shutdown Scheduler")
root.configure(bg='#2C3E50')  # Set background color

# Calculate the center position of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 450) // 2
y = (screen_height - 450) // 2

# Set the dimensions and position of the window
root.geometry(f"450x450+{x}+{y}")

# Label for user input
label = tk.Label(root, text="Select time and action:", font=("Helvetica", 14), fg='#ECF0F1', bg='#2C3E50')  # Set text and background color
label.pack()

# Frame for dropdown menus
frame = tk.Frame(root, bg='#2C3E50')  # Set background color
frame.pack(pady=10)  # Add some padding

# Dropdown menu for hours
hours_var = tk.StringVar(root)
hours_var.set("12")
hours_label = tk.Label(frame, text="Hours:", font=("Helvetica", 12), fg='#ECF0F1', bg='#2C3E50')  # Set text and background color
hours_label.grid(row=0, column=0, padx=10)  # Add padding and grid layout
hours_menu = tk.OptionMenu(frame, hours_var, *map(str, range(1, 13)))
hours_menu.grid(row=0, column=1)  # Grid layout

# Dropdown menu for minutes
minutes_var = tk.StringVar(root)
minutes_var.set("00")  # Set the default value to "00"
minutes_label = tk.Label(frame, text="Minutes:", font=("Helvetica", 12), fg='#ECF0F1', bg='#2C3E50')  # Set text and background color
minutes_label.grid(row=0, column=2, padx=10)  # Add padding and grid layout
minutes_menu = tk.OptionMenu(frame, minutes_var, *map(lambda x: f"{x:02d}", range(60)))  # Use map to add zero prefix
minutes_menu.grid(row=0, column=3)  # Grid layout

# Dropdown menu for AM/PM
period_var = tk.StringVar(root)
period_var.set("AM")
period_label = tk.Label(frame, text="AM/PM:", font=("Helvetica", 12), fg='#ECF0F1', bg='#2C3E50')  # Set text and background color
period_label.grid(row=0, column=4, padx=10)  # Add padding and grid layout
period_menu = tk.OptionMenu(frame, period_var, "AM", "PM")
period_menu.grid(row=0, column=5)  # Grid layout

# Button to initiate shutdown at a specific time
shutdown_button = tk.Button(root, text="Initiate Shutdown", command=lambda: shutdown_at(int(hours_var.get()), int(minutes_var.get()), period_var.get()), font=("Helvetica", 12), fg='#2C3E50', bg='#1ABC9C')  # Set text and background color
shutdown_button.pack(pady=10)  # Add padding

# Button to shutdown now
shutdown_now_button = tk.Button(root, text="Shutdown Now", command=lambda: os.system('shutdown /s /t 0'), font=("Helvetica", 12), fg='#2C3E50', bg='#1ABC9C')  # Set text and background color
shutdown_now_button.pack(pady=10)  # Add padding

# Button to restart now
restart_now_button = tk.Button(root, text="Restart Now", command=lambda: os.system('shutdown /r /t 0'), font=("Helvetica", 12), fg='#2C3E50', bg='#1ABC9C')  # Set text and background color
restart_now_button.pack(pady=10)  # Add padding

# Entry for specifying shutdown in minutes
minutes_entry = tk.Entry(root, font=("Helvetica", 12))
minutes_entry.pack(pady=10)

# Button to initiate shutdown in a specified number of minutes
shutdown_minutes_button = tk.Button(root, text="Shutdown in Minutes", command=lambda: shutdown_in_minutes(int(minutes_entry.get())), font=("Helvetica", 12), fg='#2C3E50', bg='#1ABC9C')  # Set text and background color
shutdown_minutes_button.pack(pady=10)  # Add padding

# Button to cancel shutdown
cancel_button = tk.Button(root, text="Cancel Shutdown", command=cancel_shutdown, font=("Helvetica", 12), fg='#2C3E50', bg='#1ABC9C')  # Set text and background color
cancel_button.pack()

# Label for countdown display
countdown_label = tk.Label(root, text="", font=("Helvetica", 16), fg='#ECF0F1', bg='#2C3E50')  # Set text and background color

# Start the main loop
root.mainloop()
