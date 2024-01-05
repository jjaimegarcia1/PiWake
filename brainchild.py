import tkinter as ui
from tkinter import ttk, messagebox
import time
import pygame

pygame.mixer.init()

window = ui.Tk()

# Center the window
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())

# Make the window full screen
window.attributes('-fullscreen', True)

# Variable to track the current color state
color_state = "yellow"
alarm_timer_id = None  # Variable to store the timer ID
flash_timer_id = None  # Variable to store the flashing timer ID


def update_clock():
    current_time = time.strftime("%I:%M:%S %p")
    digital_clock_lbl.config(text=current_time)

    # Check if the current time matches the alarm time
    if current_time == alarm_time.get():
        trigger_alarm()

    digital_clock_lbl.after(1000, update_clock)


def set_alarm():
    hour = int(hour_combobox.get())
    minute = int(minute_combobox.get())
    second = int(second_combobox.get())
    am_pm = am_pm_combobox.get()

    alarm_time_str = f"{hour:02d}:{minute:02d}:{second:02d} {am_pm}"

    alarm_time.set(alarm_time_str)

    # Changes the font color when you actually set the timer
    digital_clock_lbl.config(bg=color_state)


def flash_colors():
    global color_state, flash_timer_id

    # Toggle the color between yellow and red
    if color_state == "yellow":
        color_state = "red"
    else:
        color_state = "yellow"

    digital_clock_lbl.config(bg=color_state)

    flash_timer_id = window.after(200, flash_colors)


def trigger_alarm():
    global alarm_timer_id

    # This stuff here will be for your music
    pygame.mixer.music.load("music/JOEYDIAZalarmclock.mp3")
    pygame.mixer.music.play()

    # Start flashing the colors
    flash_colors()

    # Start the timer to update the clock
    alarm_timer_id = window.after(1000, update_clock)


def stop_alarm():
    global alarm_timer_id, flash_timer_id

    pygame.mixer.music.stop()
    digital_clock_lbl.config(bg="white")

    if alarm_timer_id is not None:
        window.after_cancel(alarm_timer_id)
        alarm_timer_id = None

    if flash_timer_id is not None:
        window.after_cancel(flash_timer_id)
        flash_timer_id = None


digital_clock_lbl = ui.Label(window, text="", font="Helvetica 72 bold")
digital_clock_lbl.grid(row=0, column=0, columnspan=4)

alarm_time = ui.StringVar()

# Combobox for hours
hour_combobox = ttk.Combobox(window, values=list(range(1, 13)), state="readonly", font=("Helvetica", 20))
hour_combobox.set("12")
hour_combobox.grid(row=1, column=0)

# Combobox for minutes
minute_combobox = ttk.Combobox(window, values=list(range(60)), state="readonly", font=("Helvetica", 20))
minute_combobox.set("00")
minute_combobox.grid(row=1, column=1)

# Combobox for seconds
second_combobox = ttk.Combobox(window, values=list(range(60)), state="readonly", font=("Helvetica", 20))
second_combobox.set("00")
second_combobox.grid(row=1, column=2)

# Combobox for AM/PM
am_pm_combobox = ttk.Combobox(window, values=["AM", "PM"], state="readonly", font=("Helvetica", 20))
am_pm_combobox.set("AM")
am_pm_combobox.grid(row=1, column=3)

# Button to set the alarm
set_alarm_btn = ui.Button(window, text="Set Alarm", command=set_alarm, font=("Helvetica", 16))
set_alarm_btn.grid(row=2, column=0, columnspan=4, pady=10)

# Button to stop the alarm
stop_alarm_btn = ui.Button(window, text="Stop Alarm", command=stop_alarm, font=("Helvetica", 16))
stop_alarm_btn.grid(row=3, column=0, columnspan=4, pady=10)

# Exit button
exit_btn = ui.Button(window, text="Exit", command=window.destroy, font=("Helvetica", 16))
exit_btn.grid(row=5, column=0, columnspan=4, pady=10)


def reset_alarm():
    global alarm_timer_id, flash_timer_id, color_state

    stop_alarm()

    # Reset the alarm time and state
    alarm_time.set("")
    color_state = "yellow"
    digital_clock_lbl.config(bg="white")  # Set the background color to your desired default color


# Add a button for resetting the alarm
reset_alarm_btn = ui.Button(window, text="Reset Alarm", command=reset_alarm, font=("Helvetica", 16))
reset_alarm_btn.grid(row=4, column=0, columnspan=4, pady=10)

update_clock()

window.mainloop()
