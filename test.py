from random import choice, randint

words = ["sex", "hate", "pain", "love", "kiwi", "lamb", "frog", "tree", "ball", "book", "moon", "fish", "bird", "rose", "star", "death", "kyiv", "lviv", "symu"]

word = choice(words)
selected_char = word[randint(0, len(word)-1)]
combination = bin(ord(selected_char))[2:]  # Convert to binary and remove '0b' prefix
combination = combination[-5:]  # Take the last 5 bits

# # Convert binary string back to ASCII character
# ascii_char = chr(int(combination, 2))

# print("Original word:", word)
# print("Selected character:", selected_char)
# print("Binary combination:", combination)
# print("Corresponding ASCII character:", ascii_char)

character_dict = {'00000': 'A', '00001': 'B', '00010': 'C', '00011': 'D', '00100': 'E', '00101': 'F', '00110': 'G', '00111': 'H', '01000': 'I', '01001': 'J', '01010': 'K', '01011': 'L', '01100': 'M', '01101': 'N', '01110': 'O', '01111': 'P', '10000': 'Q', '10001': 'R', '10010': 'S', '10011': 'T', '10100': 'U', '10101': 'V', '10110': 'W', '10111': 'X', '11000': 'Y', '11001': 'Z', '11010': '0', '11011': '1', '11100': '2', '11101': '3', '11110': '4', '11111': '5'}