import requests
from tkinter import *

# Create the main window for the weather application
root = Tk()
root.geometry("200x200+0+0")
root.title("Weather App")
root.config(bg="lightblue")
root.resizable(False, False)

# Weather icon images used for different conditions
img1 = 'img/4.png'  # default image
img2 = 'img/1.png'  # clear sky
img3 = 'img/2.png'  # clouds
img4 = 'img/3.png'  # rain


# Change the window and label background colors
def bgc(color):
    root.config(bg=color)
    des.config(bg=color)
    tem.config(bg=color)
    if color == "black":
        des.config(fg="white")
        tem.config(fg="white")
    elif color == "white":
        des.config(fg="black")
        tem.config(fg="white")          


# Read the OpenWeatherMap API key from a local text file
api_key = open("api.txt", "r").read().strip()


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
            f"https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": location,
                "units": "metric",
                "appid": api_key
            },
            timeout=10
        )

        data = res.json()
        res.raise_for_status()

        # Extract the weather description and temperature from the API response
        desp = data["weather"][0]["description"]
        temp = round(data["main"]["temp"])

        # Update the labels with the weather info
        des.config(text=desp)
        tem.config(text=f"{temp}℃")

        # Change the weather image based on the condition
        if desp == "clear sky":
            img.config(file=img2)
        elif "rain" in desp:
            img.config(file=img4)
        elif "cloud" in desp:
            img.config(file=img3)

    # Handle city not found
    except requests.exceptions.HTTPError:
        des.config(text="City not found!")
        tem.config(text="")

    # Handle other request errors
    except requests.exceptions.RequestException:
        des.config(text="error!")
        tem.config(text="")


# Input field where the user types a city name
lent = Entry(root)
lent.pack()

# Label for weather description
# (example text shown before the user searches for a city)
des = Label(root, text="enter your city", bg="lightblue")
des.pack()

# Label for temperature
# (initially empty until a city is searched)
tem = Label(root, text="", bg="lightblue")
tem.pack()

# Buttons for weather search and background color changes
# Note: The button for fetching weather is created later after the image is loaded.

# Load the default weather image for the button
img = PhotoImage(file=img1)

# Weather button with image and command to fetch weather
Bt = Button(root, text="get weather", command=weather, image=img)
Bt.pack()

# Background color buttons
bcbg = Button(root, text="black", command=lambda: bgc("black"))
bcbg.pack(side=BOTTOM)
whbg = Button(root, text="white", command=lambda: bgc("white"))
whbg.pack()
lbbg = Button(root, text="lightblue", command=lambda: bgc("lightblue"))
lbbg.pack(side=BOTTOM)


# Start the Tkinter event loop
root.mainloop()
