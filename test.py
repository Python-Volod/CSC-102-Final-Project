# from tkinter import *
# from tkinter import ttk

# class Main(ttk.Frame):
    
#     def __init__(self, window):
#         # created with help of Chat GPT
#         def decrypt_rsa():
#             ciphertext = int(c_entry.get())
#             p = int(p_entry.get())
#             q = int(q_entry.get())
#             e = int(e_entry.get())
#             def egcd(a, b):
#                 if a == 0:
#                     return (b, 0, 1)
#                 else:
#                     g, y, x = egcd(b % a, a)
#                     return (g, x - (b // a) * y, y)
#             def modinv(a, m):
#                 g, x, y = egcd(a, m)
#                 if g != 1:
#                     main_label.configure(text = 'Error occured try again')
#                     return 0
#                 else:
#                     return x % m
#             n = p * q
#             phi = (p - 1) * (q - 1)
#             d = modinv(e, phi)
#             try:
#                 plaintext = pow(ciphertext, d, n)
#                 print(plaintext)
#             except:
#                 main_label.configure(text = 'Error occured try again')
#             main_label.configure(text = "The key is {}".format(chr(plaintext)))
        
#         super().__init__(window)
#         grid(row=0, column=0)
#         # Setup two main tabs
#         tabs = ttk.Notebook(self)
#         main_tab = ttk.Frame(tabs)
#         rsa_tab = ttk.Frame(tabs)
#         tabs.add(main_tab, text="MAIN")
#         tabs.add(rsa_tab, text="RSA")
#         tabs.grid(row=0, column=0)
        

#         # Setup main tab
#         button = Button(main_tab, text="Debug RSA", command=switch_gui_to_rsa, anchor=CENTER)
#         button.grid(row=1, column=0, pady=20)

#         # Setup the RSA tab 
#         main_label = Label(rsa_tab, text="Use this in case of accidental activation", fg="green", anchor=CENTER)
#         main_label.grid(row = 0, column=0)
#         text_c= StringVar()
#         text_c.set('Enter the C-value')
#         text_e= StringVar()
#         text_e.set('Enter the E-value')
#         text_p= StringVar()
#         text_p.set('Enter the P-value')
#         text_q = StringVar()
#         text_q.set('Enter the Q-value')
#         c_entry = Entry(rsa_tab,fg="green",textvariable=text_c)
#         e_entry = Entry(rsa_tab,fg="green",textvariable=text_e)
#         p_entry = Entry(rsa_tab,fg="green",textvariable=text_p)
#         q_entry = Entry(rsa_tab,fg="green",textvariable=text_q)
#         decode_button = Button(rsa_tab, text = "Decode", command=decrypt_rsa)
#         c_entry.grid(row=1,column=0, pady=5)
#         e_entry.grid(row=2,column=0, pady=5)
#         p_entry.grid(row=3,column=0, pady=5)
#         q_entry.grid(row=4,column=0, pady=5)
#         decode_button.grid(row=5, column=0, pady=10)
#         #
#         def _erase_c_entry(event):
#             if c_entry.get() == "Enter the C-value":
#                 text_c.set("")
#         def _erase_e_entry(event):
#             if e_entry.get() == "Enter the E-value":
#                 text_e.set("")
#         def _erase_p_entry(event):
#             if p_entry.get() == "Enter the P-value":
#                 text_p.set("")
#         def _erase_q_entry(event):
#             if q_entry.get() == "Enter the Q-value":
#                 text_q.set("")

#         def _redraw_c_entry(event):
#             if c_entry.get() == "":
#                 text_c.set('Enter the C-value')
#         def _redraw_e_entry(event):
#             if e_entry.get() == "":
#                 text_e.set('Enter the E-value')
#         def _redraw_p_entry(event):
#             if p_entry.get() == "":
#                 text_p.set('Enter the P-value')
#         def _redraw_q_entry(event):
#             if q_entry.get() == "":
#                 text_q.set('Enter the Q-value')

#         #
#         c_entry.bind("<ButtonRelease-1>", _erase_c_entry)
#         e_entry.bind("<ButtonRelease-1>", _erase_e_entry)
#         p_entry.bind("<ButtonRelease-1>", _erase_p_entry)
#         q_entry.bind("<ButtonRelease-1>", _erase_q_entry)

#         c_entry.bind("<ButtonRelease-2>", _erase_c_entry)
#         e_entry.bind("<ButtonRelease-2>", _erase_e_entry)
#         p_entry.bind("<ButtonRelease-2>", _erase_p_entry)
#         q_entry.bind("<ButtonRelease-2>", _erase_q_entry)

#         c_entry.bind("<ButtonRelease-3>", _erase_c_entry)
#         e_entry.bind("<ButtonRelease-3>", _erase_e_entry)
#         p_entry.bind("<ButtonRelease-3>", _erase_p_entry)
#         q_entry.bind("<ButtonRelease-3>", _erase_q_entry)

#         c_entry.bind("<FocusOut>", _redraw_c_entry)
#         e_entry.bind("<FocusOut>", _redraw_e_entry)
#         p_entry.bind("<FocusOut>", _redraw_p_entry)
#         q_entry.bind("<FocusOut>", _redraw_q_entry)

#     def switch_gui_to_rsa(self):
#         tabs.select(rsa_tab)




# root = Tk()
# main = Main(root)
# root.title("TESTING")
# main.__init__._erase_c_entry()
# root.mainloop()

keypad_num_to_letters = {'a': '2', 'b': '22', 'c': '222', 'd': '3', 'e': '33', 'f': '333', 'g': '4', 'h': '44', 'i': '444', 'j': '5', 'k': '55', 'l': '555', 'm': '6', 'n': '66', 'o': '666', 'p': '7', 'r': '77', 's': '777', 't': '8', 'u': '88', 'v': '888', 'w': '9', 'x': '99', 'y': '999'}
_target = "love"
_target_num = ""
for l in _target:
    _target_num += keypad_letters_to_num[l]
print(_target_num)
_entered_value = ""

while True:
    _value = input("Type a number")
    if _value == _target_num[0 + len(_entered_value)]:
        _entered_value += _value
    else:
        break
    if _entered_value == _target_num:
        print("Success!")
        break


    

