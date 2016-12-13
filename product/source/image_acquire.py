from PIL import Image

items = ["android", "battery", "cloud", "cross", "dove", "electricity", "electronics", "human", "oil", "peace", "tick", "tree", "web", "wheel" ]

for i in items:

	

	out = open(i + ".txt", "w")

	im = Image.open("scaled/" + i + ".png")
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
