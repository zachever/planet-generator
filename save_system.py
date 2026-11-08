import os
import numpy as np
from PIL import Image
import json

def load_planet_from_file(file_name):
    image = Image.open(f"{file_name}")
    image_data = np.array(image)
    bits = []
    for row in image_data:
        for pixel in row:
            for channel in pixel:
                bits.append(channel & 1)

    bytes_array = []

    #i did not write the bit to byte conversion straight from google lol
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte |= bits[i + j] << j
        bytes_array.append(byte)

    #reads the number of bytes used for the settings
    size_of_settings = int(bytes_array[0]) | (int(bytes_array[1]) << 8) | (int(bytes_array[2]) << 16) | (int(bytes_array[3]) << 24)

    #crops the bytes array to only include the settings data
    bytes_array = bytes_array[4:4+size_of_settings]

    settings = json.loads(bytes(bytes_array).decode("utf-8"))
    print(settings)

    return settings

def save_planet_to_file(settings, screenshot, file_name=None):
    directory = "saved-planets"

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    if file_name is None:
        i = 0
        while True:
            file_name = f"planet_{i}.png"
            if not os.path.exists(f"{directory}/{file_name}"):
                break
            i += 1

    bytes_array = json.dumps(settings).encode("utf-8")
    size_of_settings = len(bytes_array)
    bytes_size_of_settings = [size_of_settings & 0xFF, (size_of_settings >> 8) & 0xFF, (size_of_settings >> 16) & 0xFF, (size_of_settings >> 24) & 0xFF]
    bytes_array = bytes_size_of_settings + list(bytes_array)

    #convert bytes array to bits
    bits = []
    for byte in bytes_array:
        for i in range(8):
            bits.append((byte >> i) & 1)

    #embed the bits into the screenshot image
    image_data = np.array(screenshot)
    height, width, channels = image_data.shape
    bit_index = 0
    for y in range(height):
        for x in range(width):
            for c in range(channels):
                if bit_index < len(bits):
                    #clear the last bit before we set it
                    image_data[y, x, c] &= 0b11111110
                    #set the last bit by or'ing the bit with the channel
                    image_data[y, x, c] |= bits[bit_index]
                    bit_index += 1
    image = Image.fromarray(image_data)
    image.save(f"{directory}/{file_name}")
    print(f"Saved planet to {directory}/{file_name}")