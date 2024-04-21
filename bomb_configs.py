#################################
# CSC 102 Defuse the Bomb Project
# Configuration file
# Team: 
#################################

# constants
DEBUG = True        # debug mode?
RPi = False           # is this running on the RPi?
ANIMATE = True       # animate the LCD text?
SHOW_BUTTONS = True # show the Pause and Quit buttons on the main LCD GUI?
COUNTDOWN = 480      # the initial bomb countdown value (seconds)
NUM_STRIKES = 5      # the total strikes allowed before the bomb "explodes"
NUM_PHASES = 4       # the total number of initial active bomb phases

# imports
from random import randint, shuffle, choice
from Cryptodome.Util.number import bytes_to_long
import random
import sympy
import pygame
from string import ascii_uppercase
import pygame
if (RPi):
    import board
    from adafruit_ht16k33.segments import Seg7x4
    from digitalio import DigitalInOut, Direction, Pull
    from adafruit_matrixkeypad import Matrix_Keypad

#################################
# setup the electronic components
#################################
# 7-segment display
# 4 pins: 5V(+), GND(-), SDA, SCL
#         ----------7SEG---------
if (RPi):
    i2c = board.I2C()
    component_7seg = Seg7x4(i2c)
    # set the 7-segment display brightness (0 -> dimmest; 1 -> brightest)
    component_7seg.brightness = 0.5

# keypad
# 8 pins: 10, 9, 11, 5, 6, 13, 19, NA
#         -----------KEYPAD----------
if (RPi):
    # the pins
    keypad_cols = [DigitalInOut(i) for i in (board.D10, board.D9, board.D11)]
    keypad_rows = [DigitalInOut(i) for i in (board.D5, board.D6, board.D13, board.D19)]
    # the keys
    keypad_keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))

    component_keypad = Matrix_Keypad(keypad_rows, keypad_cols, keypad_keys)

# jumper wires
# 10 pins: 14, 15, 18, 23, 24, 3V3, 3V3, 3V3, 3V3, 3V3
#          -------JUMP1------  ---------JUMP2---------
# the jumper wire pins
if (RPi):
    # the pins
    component_wires = [DigitalInOut(i) for i in (board.D14, board.D15, board.D18, board.D23, board.D24)]
    for pin in component_wires:
        # pins are input and pulled down
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

# pushbutton
# 6 pins: 4, 17, 27, 22, 3V3, 3V3
#         -BUT1- -BUT2-  --BUT3--
if (RPi):
    # the state pin (state pin is input and pulled down)
    component_button_state = DigitalInOut(board.D4)
    component_button_state.direction = Direction.INPUT
    component_button_state.pull = Pull.DOWN
    # the RGB pins
    component_button_RGB = [DigitalInOut(i) for i in (board.D17, board.D27, board.D22)]
    for pin in component_button_RGB:
        # RGB pins are output
        pin.direction = Direction.OUTPUT
        pin.value = True

# toggle switches
# 3x3 pins: 12, 16, 20, 21, 3V3, 3V3, 3V3, 3V3, GND, GND, GND, GND
#           -TOG1-  -TOG2-  --TOG3--  --TOG4--  --TOG5--  --TOG6--
if (RPi):
    # the pins
    component_toggles = [DigitalInOut(i) for i in (board.D12, board.D16, board.D20, board.D21)]
    for pin in component_toggles:
        # pins are input and pulled down
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

    component_toggles2 = [DigitalInOut(i) for i in (board.D12, board.D16, board.D20, board.D21)]
    for pin in component_toggles2:
        # pins are input and pulled down
        pin.direction = Direction.INPUT
        pin.pull = Pull.DOWN

###########
# functions
###########
# generates the bomb's serial number
#  it should be made up of alphaneumeric characters, and include at least 3 digits and 3 letters
#  the sum of the digits should be in the range 1..15 to set the toggles target
#  the first three letters should be distinct and in the range 0..4 such that A=0, B=1, etc, to match the jumper wires
#  the last letter should be outside of the range
def genSerial():
    # set the digits (used in the toggle switches phase)
    serial_digits = []
    toggle_value = randint(1, 15)
    toggles2_value = []
    # the sum of the digits is the toggle value
    while (len(serial_digits) < 3 or toggle_value - sum(serial_digits) > 0):
        d = randint(0, min(9, toggle_value - sum(serial_digits)))
        serial_digits.append(d)

    # set the letters (used in the jumper wires phase)
    jumper_indexes = [ 0 ] * 5
    while (sum(jumper_indexes) < 3):
        jumper_indexes[randint(0, len(jumper_indexes) - 1)] = 1
    jumper_value = int("".join([ str(n) for n in jumper_indexes ]), 2)
    # the letters indicate which jumper wires must be "cut"
    jumper_letters = [ chr(i + 65) for i, n in enumerate(jumper_indexes) if n == 1 ]

    # form the serial number
    serial = [ str(d) for d in serial_digits ] + jumper_letters
    # and shuffle it
    shuffle(serial)
    # finally, add a final letter (F..Z)
    toggles2_value.append([choice([chr(n) for n in range(70, 91)])])
    serial += toggles2_value
    # and make the serial number a string
    serial = "".join(serial)

    return serial, toggle_value, jumper_value
    #return serial, toggle_value, jumper_value, toggle2_value

# generates the keypad combination by encoding a random keyword using rsa
def genKeypadCombination():    
    #Generates a prime number with specified bits
    def generate_prime(bits=16):
        while True:
            p = sympy.randprime(2**(bits-1), 2**bits)
            if sympy.isprime(p):
                return p
    #Generates RSA keys
    def generate_rsa_keys():
        global p,q
        p = generate_prime()
        q = generate_prime()
        if q > p:
            p ,q = q, p
        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = random.randint(2, phi_n - 1)
        while sympy.gcd(e, phi_n) != 1:
            e = random.randint(2, phi_n - 1)
        d = sympy.mod_inverse(e, phi_n)
        return (n, e), d, [p, q]
    #Encrypts message using RSA
    def rsa_encrypt(message, public_key):
        n, e = public_key
        encoded_text = pow(bytes_to_long(message.encode()), e, n)
        return encoded_text, n, e
    # the list of keywords 
    global words 
    words = ["sex", "hate", "pain", "love", "kiwi", "lamb", "frog", "tree", "ball", "book", "moon", "fish", "bird", "rose", "star", "death", "kyiv", "lviv", "symu"]
    #Encode a random word from a list using RSA
    word = random.choice(words)
    global global_keys
    global_keys = generate_rsa_keys()
    encoded_text, n, e = rsa_encrypt(word, global_keys[0])
    return word, encoded_text, p, q, e




###############################
# generate the bomb's specifics
###############################


# generate the combination for the keypad phase
#  keyword: the plaintext keyword for the lookup table
#  cipher_keyword: the encrypted keyword for the lookup table
#  rot: the key to decrypt the keyword
#  keypad_target: the keypad phase defuse value (combination)
#  passphrase: the target plaintext passphrase
keyword, encoded_keyword, p, q, e = genKeypadCombination() # CHANGE THE COMMENTS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# generate the bomb's serial number (which also gets us the toggle and jumper target values)
#  serial: the bomb's serial number
#  toggles_target: the toggles phase defuse value
#  toggle2_target: the second toggles phase defuse value
#  wires_target: the wires phase defuse value
serial, toggles_target, wires_target = genSerial()
#serial, toggles_target, wires_target, toggles2_target = genSerial()

selected_char = keyword[randint(0, len(keyword)-1)]
combination = bin(ord(selected_char))[2:]  # Convert to binary and remove '0b' prefix
combination = combination[-5:]  # Take the last 5 bits
character_dict = {'00000': 'A', '00001': 'B', '00010': 'C', '00011': 'D', '00100': 'E', '00101': 'F', '00110': 'G', '00111': 'H', '01000': 'I', '01001': 'J', '01010': 'K', '01011': 'L', '01100': 'M', '01101': 'N', '01110': 'O', '01111': 'P', '10000': 'Q', '10001': 'R', '10010': 'S', '10011': 'T', '10100': 'U', '10101': 'V', '10110': 'W', '10111': 'X', '11000': 'Y', '11001': 'Z', '11010': '0', '11011': '1', '11100': '2', '11101': '3', '11110': '4', '11111': '5'}

wires_key = character_dict[combination]
wires_target = combination

#toggles_target = bin(toggle_value)[2:].zfill(4) # target for part 1 of toggles
#toggles2_target = bin(sum(ord(c) - 65 for c in toggle2_value))[2:].zfill(4) # target for part 2 of toggles

# generate the color of the pushbutton (which determines how to defuse the phase)
button_color = choice(["R", "G", "B"])
# appropriately set the target (R is None)
button_target = None
# G is the first numeric digit in the serial number
if (button_color == "G"):
    button_target = [ n for n in serial if n.isdigit() ][0]
# B is the last numeric digit in the serial number
elif (button_color == "B"):
    button_target = [ n for n in serial if n.isdigit() ][-1]

if (DEBUG): # check if in debug mode
    print(f"Serial number: {serial}")
    print(f"Toggles target: {bin(toggles_target)[2:].zfill(4)}/{toggles_target}")
    #print(f"Toggles2 target: {bin(toggles2_target)[2:].zfill(4)}/{toggles2_target}")
    print(f"Wires target: {bin(wires_target)[2:].zfill(5)}/{wires_target}")
    print(f"Keypad target: {keyword}, encoded as {encoded_keyword} with p:q - {p}:{q} and e : {e}")
    print(f"Button target: {button_target}")

# set the bomb's LCD bootup text
#need to change to make this go from white to green (#00ff00)
boot_text = f"Booting...\n\x00\x00"\
            f"*Kernel v3.1.4-159 loaded.\n"\
            f"Initializing subsystems...\n\x00"\
            f"*System model: 102BOMBv4.2\n"\
            f"*Serial number: {serial}\n"\
            f"Encrypting keypad...\n\x00"\
            f"*Defuse Keyword: {encoded_keyword}/ENC/10/{str(hex(int(e)))}/ENC/16/;\n*Keys:{str(bin(p))};{str(bin(q))}/ENC/2/;\n"\
            f"Rendering phases...\x00"
