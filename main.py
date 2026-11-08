import requests
from tkinter import*


root = Tk()
root.geometry("200x200+0+0")
root.title("Weather App")
root.config(bg="lightblue")

img1 = 'img/4.png'
img2 =  'img/1.png'
img3 =  'img/2.png'
img4 = 'img/3.png'


def bgc(color):
    root.config(bg=color)
    des.config(bg=color)
    tem.config(bg=color)
    if color == "black":
        des.config(fg="white")
        tem.config(bg="white")



api_key = open("api.txt", "r").read().strip()
def weather():
    location = lent.get().strip()

    if not location:
        des.config(text="Enter a city")
        return

    try:
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

        desp = data["weather"][0]["description"]
        

    
        temp = round(data["main"]["temp"])

        des.config(text=desp)
        #des2.config(text=desp2)
        tem.config(text=f"{temp}℃")


        if desp == "clear sky":
            img.config(file=img2)
        elif "rain" in desp:
            img.config(file=img4)  
        elif "cloud" in desp:
           img.config(file=img3)    


    except requests.exceptions.HTTPError:
        des.config(text="City not found!")
        tem.config(text="")

    except requests.exceptions.RequestException:
        des.config(text="error!")
        tem.config(text="")

lent = Entry(root)
lent.pack()

des = Label(root, text="enter your city", bg="lightblue")
des.pack()
#des2 = Label(root, text="", bg="lightblue")
#des2.pack()

tem = Label(root, text="", bg="lightblue")
tem.pack()

#Bt = Button(root, text="get weather", command=weather)
#Bt.pack()





img = PhotoImage(file=img1)
#limg = Label(image=img).pack()
Bt = Button(root, text="get weather", command=weather, image=img)
Bt.pack()

bcbg = Button(root, text="black", command=lambda: bgc("black"),)
bcbg.pack(side=BOTTOM)
whbg = Button(root, text="white", command=lambda: bgc("white"),)
whbg.pack()
lbbg = Button(root, text="lightblue", command=lambda: bgc("lightblue"),)
lbbg.pack(side=BOTTOM)



root.mainloop()
