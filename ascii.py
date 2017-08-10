from PIL import Image
import argparse

#terminal
parser = argparse.ArgumentParser()

parser.add_argument('file')
parser.add_argument('-o','--output')
parser.add_argument('--width', type = int, default = 80)
parser.add_argument('--height', type = int, default = 80)

#arguments
args = parser.parse_args()

IMG = args.file
HEIGHT = args.height
WIDTH = args.width
OUTPUT = args.output

ascii_char=list("!@#$%^&*(){}[]:\<>/?qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM;")

#hash
def get_char(r, g, b, alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    block = (256.0 + 1)/length 
    return ascii_char[int(gray/block)]

#main
im = Image.open(IMG)
im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

txt = ""

for i in range(HEIGHT):
	for j in range(WIDTH):
		txt += get_char(*im.getpixel((j,i)))
	txt += '\n'

print(txt)

#output
if OUTPUT:
	with open(OUTPUT,'w') as f:
		f.write(txt)
else:
	with open("output.txt",'w') as f:
		f.write(txt)


