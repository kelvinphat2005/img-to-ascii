import concurrent.futures
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

# 833 x 1200
# 833 lines, 1200 long

# 832, 1

# im.show()



true_pixels = width * height
pixels = int(true_pixels / (factor*factor))
count = 0

key = {10: " ", 9: ".", 8: "-", 7: "=", 6: "o", 5: "p", 4: "P", 3: "O", 2: "?", 1: "&", 0: "@"}

min = im.getpixel((0,0))
max = im.getpixel((0,0))

x = 0
y = 0

start = time.time()

array_size = width*height
brightness_vals = [0] * array_size
#print("array_size: ", array_size)





#print("indexes: ", indexes)



def process_with_range(ranges):
    lst = []
    
    for i in ranges:
        lst.append(process_with_index(i))
    return lst


def process_with_index(index: int):
    #x = index * factor % owidth
    x = index * factor % (owidth)
    y = int((index * factor) / owidth) * factor
    # print("index:", index,"x,", x, "y,", y)
    return process(x, y)

def process(x: int, y: int):
    avg = 0

    for i in range(factor):
        for j in range(factor):
            pixel = im.getpixel((x + i, y + j))
                
            brightness = pixel
            avg += brightness


    avg /= factor * factor
    #print(avg)

    
    #index =  (int)(y/factor) * width + (int)(x/factor)
    #brightness_vals[index] = avg
    return avg
            
def normal():
    x = 0
    y = 0
    while y < oheight:
        #print(f"Progress: {y/factor}/{height/factor}", end='\r')
        while x < owidth:
            process(x, y)

            x += factor

        y += factor
        x = 0
        

def brightness_convert():
    max = 255
    for i in range(len(brightness_vals)):
        brightness_vals[i] = int(brightness_vals[i] / max * 10)





if __name__ == "__main__":
    e = []
    divide_work = int(array_size / cores)

    prev = 0
    for i in range(cores):
        e.append(range(prev, divide_work * (i+1)))
        prev = divide_work * (i+1)
    
    result =[]
    i = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exe:
        exe.submit(process_with_range, e[i])
        i +=1
        result = exe.map(process_with_range, e)
        


    brightness_vals = []
    for i in result:
        for j in i:
            brightness_vals.append(j)

    
    
    #print(brightness_vals[0:10])
    brightness_convert()


    filename = os.path.join(dirname, 'out.txt')
    f = open(filename, "w")
    for i in brightness_vals:
        if x % width == 0:
            f.write("\n")
            #print()
            pass

        f.write(key[i])
        #print(key[i], end="")
        x += 1


    f.close()

    end = time.time()
    length = end - start
    print("It took", length, "seconds!")

    



