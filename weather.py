import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
import requests
from PIL import Image, ImageTk


#completely without AI

def main():
    app = Weather()
    app.mainloop()

class Weather(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ihat")
        self.geometry("750x450")
        self.columnconfigure((0,1,2,3), weight=1)
        self.rowconfigure((0,1,2,3), weight=1)
        self.resizable(width=False, height=False)
        #to share informations
        self.response_dictionary = {}
        self.param = {}

        #the universal style class for all the frames
        self.style = ttk.Style()
        self.style.theme_use("clam")

        #this part sets all the entries to the same style:
        self.style.configure("TEntry", font=("Helvetica", 12), padding=5, relief="flat")

        self.history = ["History:"]

        #background image of the Frame:
        #tkinter has a bug where if you try to use images in functions, the reference gets garbage collected. We have to keep a manual reference
        path = r"images\5-2-space-png-pic.png"
        image1 = self.return_image_object(path)
        if image1:            
            self.bg_image = tk.Label(self, image=image1)
            self.bg_image.place(x=0, y=0, relheight=1, relwidth=1)
            #this is the reference to the image object so that it does not get garbage collected
            self.bg_image.whatever = image1
        else:
            print("will not create label")

        # this is my API key that I will use
        self.__key = "e872f19aad18480b88994727242108"
        self._url = "http://api.weatherapi.com/v1/current.json"
        self.response_dictionary = {}

        # this is the parameter dictionary that I need for the API
        self.param = {
            "key" : self.__key,
            "q" : ""
        }

        #this is a variable to communicate the favorite city between weatherpage and main
        self.fav = ""

        # this is a dictionary to make it easier to change frames, we can change frames using keys. It has to be an instance variable, otherwise the funciton can not access it
        self.frames = {}
        #------------------------------------#
        main_frame = MainPage(self)
        main_frame.grid(row=1, column=1, columnspan=2, rowspan=2, sticky="nsew")
        self.frames[MainPage] = main_frame

        # weather_frame = WeatherPage(self)
        # weather_frame.grid(row=1, column=1, columnspan=2, rowspan=2, sticky="nsew")
        # self.frames[WeatherPage] = weather_frame
        self.generate_weather_frame()
        #------------------------------------#

        #this part of the code pushes the mainpage to be seen initially
        self.show_frame(MainPage)


    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
    #this function is so that we can keep generating WeatherPage frames
    def generate_weather_frame(self):
        weather_frame = WeatherPage(self)
        weather_frame.grid(row=1, column=1, columnspan=2, rowspan=2, sticky="nsew")
        self.frames[WeatherPage] = weather_frame
    
    def return_image_object(self, path, resize_boolean=False, resize_tuple=(0,0)):
            try:
                #this snippet of code is so that I can use the funciton to resize the images optionally
                if resize_boolean:
                    image = ImageTk.PhotoImage(Image.open(path).resize(resize_tuple))
                else:
                    image = ImageTk.PhotoImage(Image.open(path))
                return image
            except FileNotFoundError as e:
                print(f"File was not found!: {e}")
                return False
            
class MainPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.columnconfigure((0,1), weight = 1)
        self.rowconfigure((0,1,2,3), weight = 1)
        self.configure(bg="white")

        #this is a string var so I can write the city name input of the entry into another label
        self.s = tk.StringVar()



        #style layout 1
        parent.style.configure("Custom.TButton", foreground="white", background="#007BFF", font=("times new roman", 20, "bold"))
        parent.style.map("Custom.TButton", foreground = [("pressed", "dark green"), ("!pressed", "white")], background = [("active", "#0056be"), ("!pressed", "#007BFF")])

        self.title_label = ttk.Label(self, text="               Ihat's    \n          Weather App", font=("Helvetica", 20, "bold"), foreground="#182069", background="white")
        self.title_label.grid(column=1, row=0, columnspan=1, sticky="nsew")

        self.city_label = ttk.Label(self, text="\n\nCity name:", font=("Helvetica", 12, "bold"), background="white", foreground="#000000")
        self.city_label.grid(column=1, row=1, columnspan=1, sticky="nsew")

        #validation:
        city_valid = parent.register(self.validate_city)
        self.city_entry = ttk.Entry(self, textvariable=self.s, validate='all', validatecommand=(city_valid, '%P'), font=("Helvetica", 12))
        self.city_entry.grid(column=1, row=2, columnspan=1, sticky="nsew", pady=5)


        self.city_history = ttk.Combobox(self, values=parent.history, state="readonly")
        self.city_history.grid(column=1, row=2, sticky="se", pady=5)
        self.city_history.set("Your city history:")

        
        self.city_button = ttk.Button(self, text="GO", command=self.go_weather, style="Custom.TButton")
        self.city_button.grid(column=1, row=3, columnspan=1, sticky="nsew")

        #cloud icon:
        path = r"images\4834559.png"
        cloud_icon = parent.return_image_object(path, True, (100,100))
        if cloud_icon:            
            self.cloud_image = tk.Label(self, image=cloud_icon, background="white", pady=10, padx=10)
            self.cloud_image.grid(column=0, row=0, sticky="nsew")
            #this is the reference to the image object so that it does not get garbage collected
            self.cloud_image.whatever = cloud_icon
        else:
            print("will not create label")

        #city_icon
        path = r"images\360_F_1135657090_OLldcV1pIOA8jumorzwp00JnJ8VBXnGf.jpg"
        city_icon = parent.return_image_object(path, True, (80,80))
        if city_icon:            
            self.city_image = tk.Label(self, image=city_icon, background="white", pady=10, padx=10)
            self.city_image.grid(column=0, row=1, sticky="nsew")
            #this is the reference to the image object so that it does not get garbage collected
            self.city_image.whatever = city_icon
        else:
            print("will not create label")

        self.error_message = ttk.Label(self, text=" ", foreground="red", font=('Helvetica', 12, "italic"), background="white")
        self.error_message.grid(column=0, row=2, sticky="nsew")

        #this is the button that will store our favourite city
        self.twinkle = self.parent.return_image_object("images\star2.png", True, (45, 45))
        self.go_favorite_city = ttk.Button(self, text="", command=self.go_fav, image=self.twinkle, compound="left")




    def validate_city(self, city):
        if city.isalpha() or city == '\b' or city == "" or (" " in city):
            #this code snippet is so that the error message goes away once you focus in on the entry
            self.error_message.config(text="")
            return True
        else:
            return False
    def go_weather(self):
            #this function needs more work and alsp try not to hardcode urls lol
            self.parent.param['q'] = self.city_entry.get()
            # this is the actual request for the API
            response = requests.get(self.parent._url, self.parent.param)

            if response.status_code == 400:
                self.error_message.config(text=f"{self.city_entry.get()} is not a valid city")
            else:
                self.city_entry.delete(0, tk.END)
                self.parent.response_dictionary = response.json()
                #this if else is to know if WeatherPage has already been accessed and deleted, or if it is the first time it is being accessed
                if self.parent.frames[WeatherPage] != None:
                    self.parent.show_frame(WeatherPage)
                #this invokes the generate button in weather page which will allow us to code on main rather than the weather page constructor
                    self.parent.frames[WeatherPage].generate.invoke()
                else:
                    self.parent.generate_weather_frame()
                    self.parent.show_frame(WeatherPage)
                    self.parent.frames[WeatherPage].generate.invoke()

                #this is to update the history in the readpnly comobox
                self.parent.history.append(self.parent.param['q'])
                self.city_history.config(values=self.parent.history)

    def go_fav(self):
        #this is basically gonna be a copy of the go_weather function lol sorry not sorry
        self.parent.param['q'] = self.parent.fav
            # this is the actual request for the API
        response = requests.get(self.parent._url, self.parent.param)

        if response.status_code == 400:
            self.error_message.config(text=f"{self.city_entry.get()} is not a valid city")
        else:
            self.parent.response_dictionary = response.json()
            #this if else is to know if WeatherPage has already been accessed and deleted, or if it is the first time it is being accessed
            if self.parent.frames[WeatherPage] != None:
                self.parent.show_frame(WeatherPage)
            #this invokes the generate button in weather page which will allow us to code on main rather than the weather page constructor
                self.parent.frames[WeatherPage].generate.invoke()
            else:
                self.parent.generate_weather_frame()
                self.parent.show_frame(WeatherPage)
                self.parent.frames[WeatherPage].generate.invoke()
    
class WeatherPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.columnconfigure((0,1,2), weight=1)

        #this is so that we share information between classes. Weather is already initialised so we need a button to do the coding rather than coding the logic in a top-down way
        self.generate = ttk.Button(self, command=self.main)

    def main(self):
        report_current = self.parent.response_dictionary
        param = self.parent.param

        #idk why I did this, but makes it easier and i dont really need it anymore
        j = report_current

        #this variable is purely to check if the favorite button was pressed or not
        self.fav_button_pressed = 0

        #print(param, j)
        #this is the parsing part
        self.city, region, country, local_time = (j['location']['name'], j['location']['region'], j['location']['country'], j['location']['localtime'])
        temp, feels_like, is_day = (j['current']['temp_c'], j["current"]["feelslike_c"], j['current']['is_day'])
        how_is_the_weather = j["current"]["condition"]['text']
        wind_speed = j["current"]['wind_kph']
        amount_of_rain_mm = j["current"]['precip_mm']
        heat_index = j["current"]['heatindex_c']

        #this is for the scrolling feature
        self.weather_canvas = tk.Canvas(self)
        self.weather_canvas.pack(side="left", fill="both", expand=1)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.weather_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        #we need to configure the canvas now
        self.weather_canvas.configure(yscrollcommand=self.scrollbar.set)
        #very complicated but it works so eh
        self.weather_canvas.bind('<Configure>', lambda e: self.weather_canvas.configure(scrollregion=self.weather_canvas.bbox("all")))
        #now we need to put a frame into canvas
        self.canvas_frame = tk.Frame(self.weather_canvas)
        self.canvas_frame.columnconfigure((0,1), weight=1)

        #now we add the frame to it
        self.weather_canvas.create_window((0,0), window=self.canvas_frame, anchor="nw")

        #but now we have to make all the widgets inside canvas_frame (or you can still do self)
        #back arrow icon:
        path = r"images\left_arrow.png"
        back_icon = self.parent.return_image_object(path, True, (25, 25))
        if back_icon:            
            self.go_back_arrow = ttk.Button(self.canvas_frame, image=back_icon, command=self.go_main_page)
            self.go_back_arrow.grid(row=0, column=0, sticky='w')
            self.go_back_arrow.whatever = back_icon
        else:
            print("will not create Button")

        path_star1 = r"images\star1.png"
        #this path is for if the city selected is the favorite city
        path_star2 = r"images\star3.png"
        star1 = self.parent.return_image_object(path_star1, True, (35,35))
        star2 = self.parent.return_image_object(path_star2, True, (35,35))
        if star1 and star2:
            if self.parent.fav == self.city:
                self.fav_button_pressed = 1
                self.favorite = ttk.Button(self.canvas_frame, text= "favorite", image=star2, command=self.favorite_city, compound="left")
                self.favorite.grid(row=0, column=0, sticky='e')
                self.favorite.whatever = star2                
            else:
                self.favorite = ttk.Button(self.canvas_frame, text= "favorite", image=star1, command=self.favorite_city, compound="left")
                self.favorite.grid(row=0, column=0, sticky='e')
                self.favorite.whatever = star1
        else:
            print("will not create button")

        #this part of the code changes the style of the page if it is night vs day
        if is_day == 0:
            self.weather_canvas.configure(background="black")
            self.canvas_frame.configure(background="black")
            self.parent.style.configure(style= "TLabel", foreground="#ffffff", background="#000000")
            #night icon
            path = r"images\night_icon.png"
            night_icon = self.parent.return_image_object(path, True, (60, 60))
            if night_icon:            
                self.location_and_time = ttk.Label(self.canvas_frame, text=f"{country}\n{region}, {self.city}:\n{local_time}", font=("Inter", 15, "bold"), image=night_icon, compound="right")
                self.location_and_time.grid(row=1, column=0, columnspan=2, sticky="ns", padx=70, pady=10)
                self.location_and_time.whatever = night_icon
            else:
                print("will not create Button")
        else:
            self.weather_canvas.configure(background="white")
            self.canvas_frame.configure(background="white")
            self.parent.style.configure(style= "TLabel", foreground="#121212", background="#e0e0e0")
            path = r"images\day_icon.png"
            day_icon = self.parent.return_image_object(path, True, (60, 60))
            if day_icon:            
                self.location_and_time = ttk.Label(self.canvas_frame, text=f"{country}\n{region}, {self.city}:\n{local_time}", font=("Inter", 15, "bold"), image=day_icon, compound="right")
                self.location_and_time.grid(row=1, column = 0, columnspan=2, sticky="ns", padx=70, pady=10)
                self.location_and_time.whatever = day_icon
            else:
                print("will not create Button")

        #this is to determine what weather icon to choose
        if "sunny" in how_is_the_weather.lower():
            path = r"images\sunny_day.png"
            weather_icon = self.parent.return_image_object(path, True, (60, 60))
        elif "clear" in how_is_the_weather.lower():
            path = r"images\weather-clear-night (1).png"
            weather_icon = self.parent.return_image_object(path, True, (60, 60))
        elif ("cloudy" in how_is_the_weather.lower() or "overcast" in how_is_the_weather.lower()) and is_day == 1:
            path = r"images\cloudy_day.png"
            weather_icon = self.parent.return_image_object(path, True, (60, 60))
        elif ("cloudy" in how_is_the_weather.lower() or "overcast" in how_is_the_weather.lower()) and is_day == 0:
            path = r"images\cloudy_night.png"
            weather_icon = self.parent.return_image_object(path, True, (60, 60))
        elif "rain" in how_is_the_weather.lower():
            path = r"images\rainy_day.png"
            weather_icon = self.parent.return_image_object(path, True, (60, 60))
        elif "snow" in how_is_the_weather.lower():
            path = r"images\snow_icon.png"
            weather_icon = self.parent.return_image_object(path, True, (60, 60))

        # this label is for today's weather
        if weather_icon:            
            self.todays_temp = ttk.Label(self.canvas_frame, text=f"{temp}C\n{how_is_the_weather}", font=("Inter", 15, "bold"), image=weather_icon, compound="right")
            self.todays_temp.grid(row=2, column = 0, columnspan=2, sticky='ns', pady=10)
            self.todays_temp.whatever = weather_icon
        else:
            print("will not create Button")
        
        self.other_today_weather = ttk.Label(self.canvas_frame, text=f"Feels like: {feels_like}C    \nWind: {wind_speed}km/h    \nAmount of rain: {amount_of_rain_mm}mm\nHeat index: {heat_index}", font=("inter", 15, "bold"))
        self.other_today_weather.grid(row=3, column=0, columnspan=2, sticky='ns')

    def go_main_page(self):
        self.parent.show_frame(MainPage)
        #this series of code destoys the initial weatherpage frame object I made in the Weather root init method. It also replaces the dictionary value of the key WeatherPage to None so we can validate in MainPage
        self.parent.frames[WeatherPage].grid_forget()
        self.parent.frames[WeatherPage].destroy()
        self.parent.frames[WeatherPage] = None

    def favorite_city(self):
        #changes the icon to a full color star
        if self.fav_button_pressed == 0:
            self.fav_button_pressed = 1
            star = self.parent.return_image_object("images\star3.png", True, (35,35))
            self.favorite.config(image=star)
            self.favorite.whatever = star


            #x is a reference to the MainPage frame object
            x = self.parent.frames[MainPage]
            x.go_favorite_city.config(text=f"{self.city}")
            #checks if the button is already on grid
            if x.go_favorite_city.winfo_ismapped() != True:
                x.go_favorite_city.grid(row=3, column=0)

            #this assigns the city to the shared parent instance faviable 'fav'
            self.parent.fav = self.city
        else:
            #this is if fav was already pressed
            self.fav_button_pressed = 0
            star = self.parent.return_image_object("images\star1.png", True, (35,35))
            self.favorite.config(image=star)
            self.favorite.whatever = star
            
            x = self.parent.frames[MainPage]
            x.go_favorite_city.grid_forget()

            #this assigns the city to the shared parent instance faviable 'fav'
            self.parent.fav = ""         
            






if __name__ == "__main__":
    main()
