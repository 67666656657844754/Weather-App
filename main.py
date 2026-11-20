import requests
from tkinter import *

# Create the main window for the weather application
root = Tk()
root.geometry("260x280")
root.title("Weather App")
root.config(bg="lightblue")
root.resizable(False, False)

# Weather icon images used for different conditions
img_paths = {
    "default": "img/4.png",
    "clear": "img/1.png",
    "clouds": "img/2.png",
    "rain": "img/3.png",
}

# Change the window and label background colors
def bgc(color):
    root.config(bg=color)
    des.config(bg=color)
    tem.config(bg=color)

    fg_map = {
        "black": "white",
        "white": "black",
        "yellow": "red",
        "lightblue": "white",
    }
    if color in fg_map:
        des.config(fg=fg_map[color])
        tem.config(fg=fg_map[color])


# Read the OpenWeatherMap API key from a local text file
with open("api.txt", "r", encoding="utf-8") as f:
    api_key = f.read().strip()


# Fetch and display the weather for the entered city
def weather():
    location = lent.get().strip()

    # If no city was entered, show a message
    if not location:
        des.config(text="Enter a city")
        return

    try:
        # Request current weather data from OpenWeatherMap
        res = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": location,
                "units": "metric",
                "appid": api_key,
            },
            timeout=10,
        )

        res.raise_for_status()
        data = res.json()

        # Extract the weather description and temperature from the API response
        desp = data["weather"][0]["description"]
        temp = round(data["main"]["temp"])

        # Update the labels with the weather info
        des.config(text=desp)
        tem.config(text=f"{temp}℃")

        # Change the weather image based on the condition
        if desp == "clear sky":
            Bt.config(image=icons["clear"])
        elif "rain" in desp:
            Bt.config(image=icons["rain"])
        elif "cloud" in desp:
            Bt.config(image=icons["clouds"])
        else:
            Bt.config(image=icons["default"])

    # Handle city not found or invalid API key
    except requests.exceptions.HTTPError:
        des.config(text="City not found!")
        tem.config(text="")
        Bt.config(image=icons["default"])

    # Handle other request errors
    except requests.exceptions.RequestException:
        des.config(text="Error!")
        tem.config(text="")
        Bt.config(image=icons["default"])


# Input field where the user types a city name
lent = Entry(root)
lent.pack(pady=(10, 5))

# Label for weather description
des = Label(root, text="enter your city", bg="lightblue", fg="white")
des.pack()

# Label for temperature
tem = Label(root, text="", bg="lightblue", fg="white")
tem.pack(pady=(0, 5))

# Load weather images and keep references so Tkinter doesn't garbage-collect them
icons = {key: PhotoImage(file=path) for key, path in img_paths.items()}

# Weather button with image and command to fetch weather
Bt = Button(root, text="get weather", command=weather, image=icons["default"])
Bt.pack(pady=5)

fr = Frame(root, bg="lightgray", bd=2, relief=SOLID)
fr.pack(side=BOTTOM, pady=8)

# Background color buttons
Button(fr, text="black", command=lambda: bgc("black")).grid(row=0, column=0, padx=2, pady=2)
Button(fr, text="white", command=lambda: bgc("white")).grid(row=0, column=1, padx=2, pady=2)
Button(fr, text="lightblue", command=lambda: bgc("lightblue")).grid(row=0, column=2, padx=2, pady=2)
Button(fr, text="yellow", command=lambda: bgc("yellow")).grid(row=0, column=3, padx=2, pady=2)

# Start the Tkinter event loop
root.mainloop()
