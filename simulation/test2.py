from time import sleep

input_file = open("black.txt")

setx = set()
lst = []

for line in input_file:
    
    coordinate = line.strip().split(",")
    for i in range(2):
        coordinate[i] = int(coordinate[i])
    point = (coordinate[0], coordinate[1])
    setx.add(point)
    lst.append(point)

input_file.close()

"""
input_file = open("black.txt")

for line in input_file:
    coordinate = line.strip().split(",")
    for i in range(2):
        coordinate[i] = int(coordinate[i])
    point = (coordinate[0], coordinate[1])
    if point in setx:
        print("Set: yes")
    if point in lst:
        print("List: yes")
    sleep(2**-2)
"""

print(len(setx), len(lst))
print(lst)


