import clr
import time
import tkinter as tk
from tkinter import messagebox
import threading
import os  # Import the os module

dll_path = os.path.join(os.path.dirname(__file__), "OpenHardwareMonitorLib.dll")

clr.AddReference(dll_path)
from OpenHardwareMonitor import Hardware

computer = Hardware.Computer()
computer.CPUEnabled = True
computer.Open()

def get_cpu_temp():
    try:
        temps = []
        for hw in computer.Hardware:
            if hw.HardwareType == Hardware.HardwareType.CPU:
                hw.Update()
                for sensor in hw.Sensors:
                    if sensor.SensorType == Hardware.SensorType.Temperature and "core" in sensor.Name.lower():
                        if sensor.Value is not None:
                            temps.append(sensor.Value)
        return sum(temps) / len(temps) if temps else None
    except Exception as e:
        print(f"Temp read error: {e}")
        return None

def determine_color(temp):
    if temp < 60:
        return "#3df55e"  # Green
    elif temp < 75:
        return "#ffd700"  # Gold
    elif temp < 85:
        return "#ffa500"  # Orange
    elif temp < 90:
        return "#ff4500"  # OrangeRed
    else:
        return "#ff0000"  # Red

last_temp = [None]

def smooth(temp, alpha=0.2):
    if last_temp[0] is None:
        last_temp[0] = temp
    else:
        last_temp[0] = last_temp[0] * (1 - alpha) + temp * alpha
    return last_temp[0]

def update_temp(label, stop_event):
    while not stop_event.is_set():
        raw_temp = get_cpu_temp()
        temp = smooth(raw_temp) if raw_temp is not None else None
        if temp is None:
            display = "Temp read failed"
            color = "gray"
        else:
            display = f"CPU Temp: {temp:.1f} °C"
            color = determine_color(temp)

        if label.winfo_exists():  
            label.after(0, update_label, label, display, color)
        time.sleep(0.2)

def update_label(label, display, color):
    label.config(text=display, background=color)

def start_gui():
    stop_event = threading.Event() 

    def on_closing():
        stop_event.set()  
        main_window.quit() 
        main_window.destroy() 

    global main_window
    main_window = tk.Tk()
    main_window.title("CPU Temp - DigitalBrekke")
    main_window.geometry("360x230")
    main_window.resizable(False, False)

    menubar = tk.Menu(main_window)
    helpmenu = tk.Menu(menubar, tearoff=0)

    def show_about():
        messagebox.showinfo("About", "Made by: DigitalBrekke\nhttps://www.digitalbrekke.com")

    helpmenu.add_command(label="About", command=show_about)
    menubar.add_cascade(label="Info", menu=helpmenu)
    main_window.config(menu=menubar)

    label = tk.Label(main_window, text="Initializing...", font=("Helvetica", 16), anchor="center")
    label.pack(expand=True, fill="both", padx=10, pady=10)

    def on_top_slider_changed(value):
        main_window.attributes('-topmost', int(float(value)) == 1)

    top_label = tk.Label(main_window, text="Always on Top", font=("Helvetica", 12))
    top_label.pack()

    slider_frame = tk.Frame(main_window)
    slider_frame.pack()

    left_label = tk.Label(slider_frame, text="Off")
    left_label.pack(side="left", padx=5)

    top_slider = tk.Scale(
        slider_frame,
        from_=0,
        to=1,
        orient="horizontal",
        showvalue=False,
        resolution=1,
        length=50,
        command=on_top_slider_changed
    )
    top_slider.set(0)
    top_slider.pack(side="left")

    right_label = tk.Label(slider_frame, text="On")
    right_label.pack(side="left", padx=5)

    exit_button = tk.Button(main_window, text="Exit", command=on_closing)
    exit_button.pack(anchor="se", padx=15, pady=15)

    threading.Thread(target=update_temp, args=(label, stop_event), daemon=True).start()

    main_window.protocol("WM_DELETE_WINDOW", on_closing) 
    main_window.mainloop()

start_gui()
