from tkinter import *
from tkinter import ttk

class Main(ttk.Frame):
    
    def __init__(self, window):
        # created with help of Chat GPT
        def decrypt_rsa():
            ciphertext = int(self.c_entry.get())
            p = int(self.p_entry.get())
            q = int(self.q_entry.get())
            e = int(self.e_entry.get())
            def egcd(a, b):
                if a == 0:
                    return (b, 0, 1)
                else:
                    g, y, x = egcd(b % a, a)
                    return (g, x - (b // a) * y, y)
            def modinv(a, m):
                g, x, y = egcd(a, m)
                if g != 1:
                    self.main_label.configure(text = 'Error occured try again')
                    return 0
                else:
                    return x % m
            n = p * q
            phi = (p - 1) * (q - 1)
            d = modinv(e, phi)
            try:
                plaintext = pow(ciphertext, d, n)
                print(plaintext)
            except:
                self.main_label.configure(text = 'Error occured try again')
            self.main_label.configure(text = "The key is {}".format(chr(plaintext)))
        
        super().__init__(window)
        self.grid(row=0, column=0)
        # Setup two main tabs
        self.tabs = ttk.Notebook(self)
        self.main_tab = ttk.Frame(self.tabs)
        self.rsa_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.main_tab, text="MAIN")
        self.tabs.add(self.rsa_tab, text="RSA")
        self.tabs.grid(row=0, column=0)
        

        # Setup main tab
        self.button = Button(self.main_tab, text="Debug RSA", command=self.switch_gui_to_rsa, anchor=CENTER)
        self.button.grid(row=1, column=0, pady=20)

        # Setup the RSA tab 
        self.main_label = Label(self.rsa_tab, text="Use this in case of accidental activation", fg="green", anchor=CENTER)
        self.main_label.grid(row = 0, column=0)
        text_c= StringVar()
        text_c.set('Enter the C-value')
        text_e= StringVar()
        text_e.set('Enter the E-value')
        text_p= StringVar()
        text_p.set('Enter the P-value')
        text_q = StringVar()
        text_q.set('Enter the Q-value')
        self.c_entry = Entry(self.rsa_tab,fg="green",textvariable=text_c)
        self.e_entry = Entry(self.rsa_tab,fg="green",textvariable=text_e)
        self.p_entry = Entry(self.rsa_tab,fg="green",textvariable=text_p)
        self.q_entry = Entry(self.rsa_tab,fg="green",textvariable=text_q)
        self.decode_button = Button(self.rsa_tab, text = "Decode", command=decrypt_rsa)
        self.c_entry.grid(row=1,column=0, pady=5)
        self.e_entry.grid(row=2,column=0, pady=5)
        self.p_entry.grid(row=3,column=0, pady=5)
        self.q_entry.grid(row=4,column=0, pady=5)
        self.decode_button.grid(row=5, column=0, pady=10)
        #
        def _erase_c_entry(event):
            if self.c_entry.get() == "Enter the C-value":
                text_c.set("")
        def _erase_e_entry(event):
            if self.e_entry.get() == "Enter the E-value":
                text_e.set("")
        def _erase_p_entry(event):
            if self.p_entry.get() == "Enter the P-value":
                text_p.set("")
        def _erase_q_entry(event):
            if self.q_entry.get() == "Enter the Q-value":
                text_q.set("")

        def _redraw_c_entry(event):
            if self.c_entry.get() == "":
                text_c.set('Enter the C-value')
        def _redraw_e_entry(event):
            if self.e_entry.get() == "":
                text_e.set('Enter the E-value')
        def _redraw_p_entry(event):
            if self.p_entry.get() == "":
                text_p.set('Enter the P-value')
        def _redraw_q_entry(event):
            if self.q_entry.get() == "":
                text_q.set('Enter the Q-value')

        #
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

    def switch_gui_to_rsa(self):
        self.tabs.select(self.rsa_tab)




root = Tk()
main = Main(root)
root.title("TESTING")
main.__init__._erase_c_entry()
root.mainloop()