import requests
import json
import tkinter as tk
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv("key.env")
  
def get_weather(cityname, output):
    # Function to retrieve weather data and update the GUI
    # API endpoint URL
    url = "https://api.open-meteo.com/v1/forecast?latitude=43.70&longitude=1.81&hourly=temperature_2m"

    # API key
    api_key = os.getenv("API_KEY")

    url = f'http://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        output.delete(1.0, tk.END)  # Clear any previous content
        output.insert(tk.END, f'Temperature: {round(temp - 273.15,1)} C \nDescription: {desc}')
    else:
        output.delete(1.0, tk.END)
        output.insert(tk.END, 'Error fetching weather data')

def start_update(entry, output):
    # Function to start the recurring weather updates
    get_weather(entry.get(), output)
    window.after(1000, start_update, entry, output)

window = tk.Tk()
window.title("Weather App")

# Create and position the widgets
label = tk.Label(window, text="Enter city:")
label.grid(row=0, column=0)

output = tk.Text(window, height=10, width=50)
output.grid(row=2, column=0, columnspan=2)

entry = tk.Entry(window)
entry.grid(row=0, column=1)
entry.bind('<KeyRelease>', start_update(entry,output))  # Bind the update_weather function to the KeyRelease event


button = tk.Button(window, text="Get Weather", command=lambda: start_update(entry, output))
button.grid(row=1, column=0, columnspan=2)

window.mainloop()