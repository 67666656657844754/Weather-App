import requests
from tkinter import *


# Create the main window for the weather application
root = Tk()
root.geometry("200x200+0+0")
root.title("Weather App")
root['bg'] = "lightblue"

# Image paths used for different weather states
img1 = 'img/4.png'  # Default/loading image
img2 = 'img/1.png'  # Clear sky image
img3 = 'img/2.png'  # Other weather image


# Read the OpenWeatherMap API key from a local text file
api_key = open("api.txt", "r").read().strip()


def weather():
    # Get the city entered by the user and remove extra spaces
    location = lent.get().strip()

    # If the user leaves the field empty, show a message
    if not location:
        des.config(text="Enter a city")
        return

    try:
        # Request weather data from the OpenWeather API
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": location,
                "units": "metric",
                "appid": api_key
            },
            timeout=10
        )

        # Parse the JSON response
        data = res.json()
        res.raise_for_status()

        # Extract weather description and temperature from the response
        desp = data["weather"][0]["description"]
        temp = round(data["main"]["temp"])

        # Update labels with description and temperature
        des.config(text=desp)
        tem.config(text=f"{temp}℃")

        # Change the weather image based on the condition
        if desp == "clear sky":
            img.config(file=img2)
        else:
            img.config(file=img3)

    except requests.exceptions.HTTPError:
        # If the city is not found, show a message
        des.config(text="City not found!")
        tem.config(text="")

    except requests.exceptions.RequestException:
        # Handle any other request errors
        des.config(text="error!")
        tem.config(text="")


# Input field for the city name
lent = Entry(root)
lent.pack()

# Label for weather description text
des = Label(root, text="enter your city", bg="lightblue")
des.pack()

# Label for temperature value
tem = Label(root, text="", bg="lightblue")
tem.pack()

# Button to fetch the weather for the entered city
Bt = Button(root, text="get weather", command=weather)
Bt.pack()


# Display the default image at startup
img = PhotoImage(file=img1)
limg = Label(image=img).pack()


# Start the Tkinter event loop
root.mainloop()
