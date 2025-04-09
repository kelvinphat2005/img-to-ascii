import numpy as np

import mmap

from PIL import Image
import time
import os


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'input.png')

# converts image to greyscale ('L')
im = Image.open(filename).convert('L')
# downscale factor
factor = 4
cores = 8
owidth, oheight = im.size # old width height

# part of the image will be cut off =(
if owidth % factor != 0:
    owidth -= owidth % factor
if oheight % factor != 0:
    oheight -= oheight % factor


width = int(owidth / factor)
height = int(oheight / factor)

true_pixels = width * height
pixels = int(true_pixels / (factor*factor))

key = {10: " ", 9: ".", 8: "-", 7: "=", 6: "o", 5: "p", 4: "P", 3: "O", 2: "?", 1: "&", 0: "@"}

array_size = width*height
brightness_vals = [0] * array_size
# brightness_vals.append(0) # first index will be used an a counter
brightness_vals = np.array(brightness_vals)

def process(x: int, y: int):
    avg = 0
    # process pixel in a factor x factor area
    # average out brightness in that area
    for i in range(factor):
        for j in range(factor):
            try:
                pixel = im.getpixel((x + i, y + j))

                brightness = pixel
                avg += brightness
            except:
                return -1

    avg /= factor * factor
    return int(avg)


def worker_range(rangex, file):
    #print("WORKER","STARTED")
    for i in range(rangex[0], rangex[1]):
        #print(i)
        worker(i, file)



def worker(id : int, file):
    # due to +1 width
    # check if the worker is working on that +1
    # add '\n' if so
    if id % (width) == 0:
        #print("new line")
        char = '\n'
        file[id] = ord(char)
        return
    
    # use the id to get the corresponding x and y coords
    x = (id * factor) % owidth
    y = int((id / width) * factor)

    # invalid result
    # return
    result = process(x, y)

    # convert a value within a range of 0-255
    # to a value within a range of 0-10
    converted_brightness_int = int((10*result)/255)
    char = key[converted_brightness_int]
    #print(id, char, ord(char))
    file[id] = ord(char)

if __name__ == "__main__":
    start = time.time()
    
    # add additional width so there is room to add '\n'
    # make sure to change processing accordingly
    width += 1


    filename = os.path.join(dirname, "bytewrite_out.txt")
    file = open(filename, "r+b")
    mmapped_file = mmap.mmap(file.fileno(), width * height)

    v = width * height
    worker_range([0, v], mmapped_file)
    

    mmapped_file.flush()

    end = time.time()
    length = end - start
    print("It took", length, "seconds!")
