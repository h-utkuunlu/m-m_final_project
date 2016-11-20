from PIL import Image

out = open("black.txt", "w")

im = Image.open("question_mark.jpg")
pix = im.load()
#print(im.size)

for x in range(im.size[0]):
    for y in range(im.size[1]):
        if pix[x,y] == (0, 0, 0):
            print((x,y), file=out)
        
out.close()
