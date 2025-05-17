import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import datetime
from collections import defaultdict
API_KEY = "4529fb80983829acc1afc6da22e1f8da"
def get_forecast():
    city = city_entry.get()
    if not city:
        result_label.config(text="Enter a city name.")
        return
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        result_label.config(text="City not found or API error.")
        return
    data = response.json()
    forecasts = data["list"]
    daily_data = defaultdict(list)
    for item in forecasts:
        date = item["dt_txt"].split(" ")[0]
        daily_data[date].append(item)
    for widget in forecast_frame.winfo_children():
        widget.destroy()
    icons.clear()
    for i, (date, entries) in enumerate(list(daily_data.items())[:5]):
        day = datetime.strptime(date, "%Y-%m-%d").strftime("%a\n%d %b")
        temp = entries[0]["main"]["temp"]
        desc = entries[0]["weather"][0]["description"]
        icon_code = entries[0]["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icons.append(icon_photo)
        # Weather card
        block = tk.Frame(forecast_frame, bg="#2b2b2b", bd=1, relief="groove", padx=10, pady=10)
        block.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
        tk.Label(block, text=day, font=("Helvetica", 10, "bold"), fg="white", bg="#2b2b2b").pack()
        tk.Label(block, image=icon_photo, bg="#2b2b2b").pack()
        tk.Label(block, text=f"{temp:.1f}°C", font=("Helvetica", 12), fg="white", bg="#2b2b2b").pack()
        tk.Label(block, text=desc, wraplength=100, justify="center", fg="lightgray", bg="#2b2b2b").pack()
    for i in range(5):
        forecast_frame.grid_columnconfigure(i, weight=1)
#gui
root = tk.Tk()
root.title("5-Day Weather Forecast - Dark Mode")
root.geometry("800x300")
root.configure(bg="#1e1e1e")
city_entry = tk.Entry(root, width=30, bg="#2b2b2b", fg="white", insertbackground="white", relief="flat")
city_entry.pack(pady=10)
get_btn = tk.Button(root, text="Get Forecast", command=get_forecast, bg="#444", fg="white", activebackground="#666",relief="flat")
get_btn.pack()
result_label = tk.Label(root, text="", fg="red", bg="#1e1e1e")
result_label.pack()
forecast_frame = tk.Frame(root, bg="#1e1e1e")
forecast_frame.pack(fill="both", expand=True, padx=10, pady=10)
icons = []
root.mainloop()