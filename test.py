from tkinter import * 
from PIL import ImageTk, Image

class Lcd(Frame):

    def __init__(self, window, m_player = 1):
        super().__init__(window, bg="black")
        self.window = window
        self.window.configure(bg='black')
        self._intro_text = Label(self.window, bg="black", fg="#00ff00", font=("Courier New", 18), text="DEVICE ACTIVATION HAS BEEN INITIATED")
        #loading screen + loading intro text
        self.img_intro = Image.open("visual/stalker.gif")
        self.img_intro = self.img_intro.resize((200, 200), Image.Resampling.LANCZOS)
        self.img_intro = ImageTk.PhotoImage(self.img_intro)
        self.img_portal = Image.open("visual/portal2.png")
        self.img_portal = self.img_portal.resize((20, 20), Image.Resampling.LANCZOS)
        self.img_portal = ImageTk.PhotoImage(self.img_portal)
        self._introlabel = Label(self.window, bg= "black", image=self.img_intro)
        self._secret = Label(self.window, bg= "black", image=self.img_portal)
        self._introlabel.place(relx=0.37, rely=0.30)
        self._secret.place(relx=0, rely=0.95)
        self._intro_text.place(relx=0.18, rely=0.15)

# Create root window
root = Tk()
lcd = Lcd(root)
root.attributes("-fullscreen", True)  # Set fullscreen attribute after initializing the Lcd object
root.update()
root.mainloop()
