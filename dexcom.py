from pydexcom import Dexcom
from PIL import ImageTk, Image as Imager
import tkinter, math, time, json

data = ""

with open("login.json", "r") as file:
    data = json.load(file)
    
dexcom = Dexcom(username=data["username"], password=data["password"], region="ous") 
TRANSPARENT = "gray1"    

class Image(tkinter.Label):
    def __init__(self, image, size, position, master):
        tkinter.Label.__init__(self, master)
        self.img = ImageTk.PhotoImage(Imager.open(image).resize((size)))

        self.configure(background=TRANSPARENT, image=self.img)
        self.place(relx=position[0], rely=position[1], anchor="center")


class CGM_Text(tkinter.Label):
    def __init__(self, size, master):
        tkinter.Label.__init__(self, master)
        self.font = "Comic Sans MS"
        self.default_size = size
        self.configure(text = self.get_data())
        self.configure(font=(self.font, size), background="white", fg="black")
        self.place(relx=.5, rely=.5, relheight=.4, relwidth=.7, anchor="center")


    def get_data(self):
        reading = dexcom.get_current_glucose_reading()
        return str(math.floor(((reading.value)/18) * 10) / 10)
    
    def set_text(self, text, fontsize):
        self.configure(text = text, font=(self.font, fontsize))

    def refresh_cgm(self):
        print("updating")
        self.set_text("updating...", 9)
        self.after(1000, lambda: self.set_text(self.get_data(), self.default_size))
        
        self.after(60000, self.refresh_cgm)


class DragLabel(tkinter.Canvas):
    def __init__(self, master=None):
        tkinter.Canvas.__init__(self, master)
        self._x = 0
        self._y = 0
        self.pack()

        self.configure(background=TRANSPARENT, highlightthickness=0)
       

        self.head_label = Image("img/bighead.png", (60,60), (.7, .5), self)
        self.bubble_label = Image("img/bubble.png", (100, 70), (.46, .43), self)

        self.cgm_val = CGM_Text(20, self.bubble_label)
        self.cgm_val.refresh_cgm()
        

        self.head_label.bind("<B1-Motion>", self.movetext)
        self.head_label.bind("<ButtonPress-1>", self.startmove)

    def startmove(self, event):
        self._x = event.x
        self._y = event.y


    def movetext(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x_pos  = self.winfo_x() + deltax
        y_pos = self.winfo_y() + deltay

        self.place(x=x_pos, y=y_pos)

class App(tkinter.Tk):
    def __init__(self, master=None):
        tkinter.Tk.__init__(self, master)

        self.wm_attributes("-fullscreen", True)
        self.wm_attributes("-transparentcolor", TRANSPARENT)
        self.wm_attributes("-topmost", True)


        canvas = tkinter.Canvas(self, bg = TRANSPARENT, highlightthickness=0)
        canvas.pack(fill=tkinter.BOTH, expand=True)

        self.text = DragLabel()
        
        canvas.create_window(100, 100, window=self.text, anchor="w")
    
    



app = App()
app.mainloop()