import pygame
import math
from random import choice, randint
from time import sleep

input_file = open("black.txt")
set_on = set()

for line in input_file:
    
    coordinate = line.strip().split(",")
    for i in range(2):
        coordinate[i] = int(coordinate[i])
    point = (coordinate[0], coordinate[1])
    set_on.add(point)

print(len(set_on))
#print(len(black))

pygame.init()
screen = pygame.display.set_mode((800, 400))

cenx = screen.get_width()//2
ceny = screen.get_height()//2

white = (255, 255, 255)
gray = (150, 150, 150)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

total_step = 256
pi = math.pi

play = True

alpha = 0
d_alpha = 1
beta = pi/2
d_beta = 1


r = 90 # 30 * 3

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]

#print(prime1, prime2)

screen.fill(white)

while play:

    
    prime1 = choice(primes)
    prime2 = choice(primes)
    
    print(prime1, prime2)
    
    i = 0
    
    while i < 667:    
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                break
           
        #Pendulum arm tip pos calculation
        temp_x = r * (math.cos(alpha) + math.cos((3*pi/2)+ alpha + beta))
        temp_y = r * (math.sin(alpha) + math.sin((3*pi/2)+ alpha + beta))
        p_tip = (int(cenx + temp_x), int(ceny + temp_y))
        p_check = (int(temp_x), int(temp_y))
        beta += prime1*((2*pi)/total_step)
        
        #Main arm tip pos calculation
        temp_x = r * math.cos(alpha)
        temp_y = r * math.sin(alpha)
        m_tip = (int(cenx + temp_x), int(ceny + temp_y))
        alpha += prime2*((2*pi)/total_step)
        
        #print((p_tip[0] - cenx), (p_tip[1] - ceny))
        
        #screen.fill(black)
        
        #Base
        #pygame.draw.line(screen, gray, (cenx, ceny), (cenx, ceny + 180 + 20), 1)
        #pygame.draw.line(screen, gray, (cenx - 30, ceny + 180 + 20), (cenx + 30, ceny + 180 + 20), 1)
        
        #Main arm
        #pygame.draw.line(screen, white, (cenx, ceny), m_tip, 1)
        
        #Pendulum arm
        #pygame.draw.line(screen, white, m_tip, p_tip, 1)
        
        #Tips
        #pygame.draw.circle(screen, red, m_tip, 1)
        pygame.draw.circle(screen, (randint(0, 255), randint(0, 255), randint(0, 255)), p_tip, 1)
        
        pygame.display.update()
        sleep(2**-10)
        i += 1
        
    sleep(3)
    screen.fill(white)
    
pygame.display.quit()
