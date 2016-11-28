from PIL import Image

out = open("black.txt", "w")

im = Image.open("test_image.jpg")
pix = im.load()
print(im.size)

for x in range(im.size[0]):
	for y in range(im.size[1]):
		if pix[x,y] == (0, 0, 0):
			temp_x = int(x)
			temp_y = int(y)
			string = str(temp_x) + "," + str(temp_y)
			print(string, file=out)
out.close()
