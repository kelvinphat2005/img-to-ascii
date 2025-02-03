from PIL import Image
import time
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'input.png')

# converts image to greyscale ('L')
im = Image.open(filename).convert('L')
# integer scaling factor
factor = 4
owidth, oheight = im.size # old width height

# part of the image will be cut off =(
if owidth % factor != 0:
    owidth -= owidth % factor
if oheight % factor != 0:
    oheight -= oheight % factor


width = int(owidth / factor)
height = int(oheight / factor)


print("Old:")
print(owidth, oheight)
print("New:")
print(width, height)
print(width*height)

true_pixels = width * height
pixels = int(true_pixels / (factor*factor))
count = 0

brightness_vals = []

key = {10: " ", 9: ".", 8: "*", 7: ":", 6: "c", 5: "o", 4: "P", 3: "O", 2: "?", 1: "&", 0: "@"}





def main():
    start = time.time()

    min = im.getpixel((0,0))
    max = im.getpixel((0,0))

    x = 0
    y = 0

    while y < oheight:
        #print(f"Progress: {y/factor}/{height/factor}", end='\r')
        while x < owidth:
            avg = 0 
            
            #print(x, y)
            for i in range(factor):
                for j in range(factor):
                    
                    pixel = im.getpixel((x + i, y + j))
                    
                    brightness = pixel
                    avg += brightness

            avg /= factor * factor

            if avg > max:
                max = avg
            if avg < min:
                min = avg
            brightness_vals.append(avg)

            x += factor

        y += factor
        x = 0
            
    print(min)
    print(max)
    for i in range(len(brightness_vals)):
        brightness_vals[i] = int(brightness_vals[i] / max * 10)





    x = 0
    y = 0

    #print(brightness_vals)

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

if __name__ == "__main__":
    main()