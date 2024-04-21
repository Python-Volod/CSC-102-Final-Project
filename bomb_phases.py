#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################
import tkinter.ttk
from pydub import AudioSegment
from pydub.playback import play

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
from PIL import ImageTk, Image
import tkinter
from threading import Thread
from time import sleep
import os
import sys


#########
# functions
#########


def decrypt_rsa(c_entry, p_entry, q_entry, e_entry, main_label):
    ciphertext = int(c_entry.get())
    p = int(p_entry.get())
    q = int(q_entry.get())
    e = int(e_entry.get())

    try:
        n = p * q
        # Calculate phi(n)
        phi = (p - 1) * (q - 1)

        # Calculate the modular multiplicative inverse of e modulo phi(n) to find d
        d = sympy.mod_inverse(e, phi)
    except:
        main_label.configure(text='Error occurred. Try again.')
        return
        # Decrypt the ciphertext
    try:
        plaintext = pow(ciphertext, d, n)
    except:
        main_label.configure(text='Error occurred. Try again.')
        return
    plaintext_string = ""
    while plaintext:
        plaintext_string += chr(plaintext & 0xFF)
        plaintext >>= 8
    plaintext_string = plaintext_string[::-1]
    if (plaintext_string not in words):
        if ([p, q] == global_keys[2]) and (ciphertext == encoded_keyword):
            main_label.configure(text="The key is {}".format(keyword))
            return
        else:
            main_label.configure(text="Incorect input, try again")
            return
    main_label.configure(text="The key is {}".format(plaintext_string))


#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    pygame.init()

    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.setupBoot()

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        # create two main tabs of GUI, one for general information and the other is for RSA decryption
        self.tabs = tkinter.ttk.Notebook(self)
        self.main_tab = tkinter.Frame(self.tabs, bg="black")
        self.rsa_tab = tkinter.Frame(self.tabs, bg="black")
        self.tabs.add(self.main_tab, text="MAIN")
        self.tabs.add(self.rsa_tab, text="RSA")
        self.tabs.pack(fill=BOTH, expand=1)
        self.main_tab.columnconfigure(0, weight=1)
        self.main_tab.columnconfigure(1, weight=2)
        self.main_tab.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        # Setup the main_tab
        # the timer
        self._ltimer = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18), text="Keypad phase: ")
        self._lkeypad.grid(row=2, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18), text="Wires phase: ")
        self._lwires.grid(row=3, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18), text="Button phase: ")
        self._lbutton.grid(row=4, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18),
                               text="Toggles phase: ")
        self._ltoggles.grid(row=5, column=0, columnspan=2, sticky=W)

        '''
        self._ltoggles2 = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18),
                               text="Toggles phase: ")
        self._ltoggles2.grid(row=5, column=0, columnspan=2, sticky=W)
        '''

        # the strikes left
        self._lstrikes = Label(self.main_tab, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=5, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self.main_tab, bg="red", fg="white", font=("Courier New", 18), text="Pause",
                                          anchor=CENTER, command=self.pause)
            self._bpause.grid(row=6, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self.main_tab, bg="red", fg="white", font=("Courier New", 18), text="Quit",
                                         anchor=CENTER, command=self.quit)
            self._bquit.grid(row=6, column=2, pady=40)
        # Setup the RSA tab 
        # Main function for the RSA that decrypts using user entered values 
        # created created with help of Chat GPT
        # Feedback for the user
        self.main_label = Label(self.rsa_tab, text="Use this in case of accidental activation", fg="#00ff00",
                                anchor=CENTER, font=("Courier New", 18), bg="black")
        self.main_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.img1 = Image.open("visual/rad_dan.png")
        self.img1 = self.img1.resize((150, 150), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.left_image_label = Label(self.rsa_tab, image=self.img1, height=150, width=150, bg="black")
        self.right_image_label = Label(self.rsa_tab, image=self.img1, height=150, width=150, bg="black")
        self.left_image_label.place(relx=0.05, rely=0.5)
        self.right_image_label.place(relx=0.75, rely=0.5)
        # self.right_image_label.place(relx=0.75, rely=0.45)
        # Fields for user to enter values and button to decode using the given information
        self.text_c = StringVar()
        self.text_c.set('Enter the C-value')
        self.text_e = StringVar()
        self.text_e.set('Enter the E-value')
        self.text_p = StringVar()
        self.text_p.set('Enter the P-value')
        self.text_q = StringVar()
        self.text_q.set('Enter the Q-value')
        self.c_entry = Entry(self.rsa_tab, fg="#00ff00", textvariable=self.text_c, font=("Courier New", 18),
                             bg="dim gray", relief=SUNKEN)
        self.e_entry = Entry(self.rsa_tab, fg="#00ff00", textvariable=self.text_e, font=("Courier New", 18),
                             bg="dim gray", relief=SUNKEN)
        self.p_entry = Entry(self.rsa_tab, fg="#00ff00", textvariable=self.text_p, font=("Courier New", 18),
                             bg="dim gray", relief=SUNKEN)
        self.q_entry = Entry(self.rsa_tab, fg="#00ff00", textvariable=self.text_q, font=("Courier New", 18),
                             bg="dim gray", relief=SUNKEN)
        self.decode_button = tkinter.Button(self.rsa_tab, text="Decode",
                                            command=lambda: decrypt_rsa(self.c_entry, self.p_entry, self.q_entry,
                                                                        self.e_entry, self.main_label),
                                            font=("Courier New", 18), bg="firebrick4")
        self.c_entry.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.e_entry.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.p_entry.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.q_entry.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.decode_button.place(relx=0.5, rely=0.9, anchor=CENTER)

        # Create events so that the empty entry fields would show what values they excpect
        def _erase_c_entry(event):
            if self.c_entry.get() == "Enter the C-value":
                self.text_c.set("")

        def _erase_e_entry(event):
            if self.e_entry.get() == "Enter the E-value":
                self.text_e.set("")

        def _erase_p_entry(event):
            if self.p_entry.get() == "Enter the P-value":
                self.text_p.set("")

        def _erase_q_entry(event):
            if self.q_entry.get() == "Enter the Q-value":
                self.text_q.set("")

        def _redraw_c_entry(event):
            if self.c_entry.get() == "":
                self.text_c.set('Enter the C-value')

        def _redraw_e_entry(event):
            if self.e_entry.get() == "":
                self.text_e.set('Enter the E-value')

        def _redraw_p_entry(event):
            if self.p_entry.get() == "":
                self.text_p.set('Enter the P-value')

        def _redraw_q_entry(event):
            if self.q_entry.get() == "":
                self.text_q.set('Enter the Q-value')

        self.c_entry.bind("<ButtonRelease-1>", _erase_c_entry)
        self.e_entry.bind("<ButtonRelease-1>", _erase_e_entry)
        self.p_entry.bind("<ButtonRelease-1>", _erase_p_entry)
        self.q_entry.bind("<ButtonRelease-1>", _erase_q_entry)

        self.c_entry.bind("<ButtonRelease-2>", _erase_c_entry)
        self.e_entry.bind("<ButtonRelease-2>", _erase_e_entry)
        self.p_entry.bind("<ButtonRelease-2>", _erase_p_entry)
        self.q_entry.bind("<ButtonRelease-2>", _erase_q_entry)

        self.c_entry.bind("<ButtonRelease-3>", _erase_c_entry)
        self.e_entry.bind("<ButtonRelease-3>", _erase_e_entry)
        self.p_entry.bind("<ButtonRelease-3>", _erase_p_entry)
        self.q_entry.bind("<ButtonRelease-3>", _erase_q_entry)

        self.c_entry.bind("<FocusOut>", _redraw_c_entry)
        self.e_entry.bind("<FocusOut>", _redraw_e_entry)
        self.p_entry.bind("<FocusOut>", _redraw_p_entry)
        self.q_entry.bind("<FocusOut>", _redraw_q_entry)

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        #self._ltoggles2.destroy()
        self._lstrikes.destroy()
        self.rsa_tab.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self.main_tab, bg="red", fg="white", font=("Courier New", 18), text="Retry",
                                      anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self.main_tab, bg="red", fg="white", font=("Courier New", 18), text="Quit",
                                     anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)


# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False


# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"


class M_Player(PhaseThread):
    def __init__(self, song, name="M_Player", factor=1):
        super().__init__(name)
        self.current_song = song
        self.factor = factor
        self._running = True

    def run(self, n=-1):
        # Load the audio file
        sound = AudioSegment.from_file("sounds/" + self.current_song)

        # Adjust speed using the factor
        sound_with_adjusted_speed = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * self.factor)
        })
        sound_with_adjusted_speed = sound_with_adjusted_speed[:50000]
        play(sound_with_adjusted_speed)
        if self._running == True:
            self.factor += 50 / COUNTDOWN
            self.run()


# the keypad phase
class Keypad(PhaseThread):

    def __init__(self, component, target, gui, name="Keypad"):
        super().__init__(name, component, target)
        self._location = "main"
        # the default value is an empty string
        self._value = ""
        self._entered_value = ""
        self.counter = 1
        self.gui = gui
        self.keypad_letters_to_num = {'a': '2', 'b': '22', 'c': '222', 'd': '3', 'e': '33', 'f': '333', 'g': '4',
                                      'h': '44', 'i': '444', 'j': '5', 'k': '55', 'l': '555', 'm': '6', 'n': '66',
                                      'o': '666', 'p': '7', 'r': '77', 's': '777', 't': '8', 'u': '88', 'v': '888',
                                      'w': '9', 'x': '99', 'y': '999'}
        self._target_num = ""
        for l in self._target:
            self._target_num += self.keypad_letters_to_num[l]

    def switch_location(self):
        if self.counter == 1:
            self.gui.tabs.select(self.gui.rsa_tab)
            self.gui.update()
            self._location = "rsa_tab_c"
        if self.counter == 2:
            self._location = "rsa_tab_e"
        if self.counter == 3:
            self._location = "rsa_tab_p"
        if self.counter == 4:
            self._location = "rsa_tab_q"
        if self.counter == 5:
            self._location = "rsa_tab_button"
        if self.counter == 6:
            self.gui.tabs.select(self.gui.main_tab)
            self._location = "main"
            self.gui.update()
            self.counter = 0
        self.counter += 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                # log the key
                self._value += str(key)
                if self._value == "*":
                    self.switch_location()
                    self._value = ""
                elif self._location == "main":
                    # the combination is correct -> phase defused
                    if self._value == self._target_num[0 + len(self._entered_value)]:
                        self._entered_value += self._value
                        if self._entered_value == self._target_num:
                            self._defused = True
                        self._value = ""
                        pass
                    # the combination is incorrect -> phase failed (strike)
                    else:
                        self._failed = True
                        self._entered_value = ""
                elif self._location == "rsa_tab_c":
                    if self.gui.c_entry.get() == "Enter the C-value":
                        self.gui.text_c.set("")
                    elif self._value == "#":
                        prev = self.gui.c_entry.get()
                        prev = prev[:len(prev) - 1]
                        self.gui.text_c.set(prev)
                        self._value = ""
                        if prev == "":
                            self.gui.text_c.set('Enter the C-value')
                    prev = self.gui.c_entry.get()
                    self.gui.text_c.set(prev + self._value)
                    self._value = ""
                elif self._location == "rsa_tab_e":
                    if self.gui.e_entry.get() == "Enter the E-value":
                        self.gui.text_e.set("")
                    elif self._value == "#":
                        prev = self.gui.e_entry.get()
                        prev = prev[:len(prev) - 1]
                        self.gui.text_e.set(prev)
                        self._value = ""
                        if prev == "":
                            self.gui.text_e.set('Enter the E-value')
                    prev = self.gui.e_entry.get()
                    self.gui.text_e.set(prev + self._value)
                    self._value = ""
                elif self._location == "rsa_tab_p":
                    if self.gui.p_entry.get() == "Enter the P-value":
                        self.gui.text_p.set("")
                    elif self._value == "#":
                        prev = self.gui.p_entry.get()
                        prev = prev[:len(prev) - 1]
                        self.gui.text_p.set(prev)
                        self._value = ""
                        if prev == "":
                            self.gui.text_p.set('Enter the P-value')
                    prev = self.gui.p_entry.get()
                    self.gui.text_p.set(prev + self._value)
                    self._value = ""
                elif self._location == "rsa_tab_q":
                    if self.gui.q_entry.get() == "Enter the Q-value":
                        self.gui.text_q.set("")
                    elif self._value == "#":
                        prev = self.gui.q_entry.get()
                        prev = prev[:len(prev) - 1]
                        self.gui.text_q.set(prev)
                        self._value = ""
                        if prev == "":
                            self.gui.text_q.set('Enter the Q-value')
                    prev = self.gui.q_entry.get()
                    self.gui.text_q.set(prev + self._value)
                    self._value = ""
                elif self._location == "rsa_tab_button":
                    if self._value == "#":
                        decrypt_rsa(self.gui.c_entry, self.gui.p_entry, self.gui.q_entry, self.gui.e_entry,
                                    self.gui.main_label)
                        self.gui.update()
                    self._value = ""
            sleep(0.1)

    # returns the keypad combination as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED, key: " + wires_key
        else:
            return self._entered_value


# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            self._value = ""
            # get the pushbutton's state
            for wire in self._component:
                if wire.value == True:
                    self._value += "1"
                else:
                    self._value += "0"
            if self._value == "11111":
                sleep(0.1)
            elif self._value == self._target:
                self._defused = True
            else:
                print("Third case---------")
                n = 0
                for wire in self._value:
                    print(wire)
                    if wire == self._target[n]:
                        None
                    elif wire == "0":
                        self._failed = True
                    n += 1
            sleep(0.1)

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return self._value


# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer

    # runs the thread
    def run(self):
        self._running = True
        # set the RGB LED color
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (self._running):
            # get the pushbutton's state
            self._value = self._component.value
            # it is pressed
            if (self._value):
                # note it
                self._pressed = True
            # it is released
            else:
                # was it previously pressed?
                if (self._pressed):
                    # check the release parameters
                    # for R, nothing else is needed
                    # for G or B, a specific digit must be in the timer (sec) when released
                    if (not self._target or self._target in self._timer._sec):
                        self._defused = True
                    else:
                        self._failed = True
                    # note that the pushbutton was released
                    self._pressed = False
            sleep(0.1)

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")


# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        self._running = True
        self._value = ""
        while (self._running):
            # the combination is correct -> phase defused
            if (
                    self._value == self._target) and button_color != "B":  # correct combination + check if button target is correct
                self._defused = True
            # the combination is incorrect -> phase failed (strike)
            else:
                self._failed = True
        sleep(0.1)

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return "ARMED"
            # TODO

'''
class Toggles2(PhaseThread):
    def __init__(self, component, target, name="Toggles2"):
        super().__init__(name, component, target)

    # runs the thread
    def run(self):
        self._running = True
        self._value = ""
        while (self._running):
            # the combination is correct -> phase defused
            if (
                    self._value == self._target) and button_color != "B":  # correct combination + check if button target is correct
                self._defused = True
            # the combination is incorrect -> phase failed (strike)
            else:
                self._failed = True
        sleep(0.1)

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            return "ARMED"
            # TODO
'''
