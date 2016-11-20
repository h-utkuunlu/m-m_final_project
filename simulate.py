import pygame
import math
from time import sleep

pygame.init()
screen = pygame.display.set_mode((1024, 576))

cenx = screen.get_width()//4
ceny = screen.get_height()//2

white = (255, 255, 255)
gray = (150, 150, 150)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

total_step = 256

play = True

alpha = 0
d_alpha = 1
beta = 0
d_beta = 1
pi = math.pi

r = 90 # 30 * 3

while play:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            break
    
    #Pendulum arm tip pos calculation
    temp_x = r * (math.cos(alpha) + math.cos((3*pi/2)+ alpha + beta))
    temp_y = r * (math.sin(alpha) + math.sin((3*pi/2)+ alpha + beta))
    p_tip = (int(cenx + temp_x), int(ceny + temp_y))
    beta += 19/total_step
    
    #Main arm tip pos calculation
    temp_x = r * math.cos(alpha)
    temp_y = r * math.sin(alpha)
    m_tip = (int(cenx + temp_x), int(ceny + temp_y))
    alpha += 17/total_step
    
    screen.fill(black)
    
    #Base
    pygame.draw.line(screen, gray, (cenx, ceny), (cenx, ceny + 180 + 20), 3)
    pygame.draw.line(screen, gray, (cenx - 30, ceny + 180 + 20), (cenx + 30, ceny + 180 + 20), 3)
    
    #Main arm
    pygame.draw.line(screen, white, (cenx, ceny), m_tip, 3)
    
    #Pendulum arm
    pygame.draw.line(screen, white, m_tip, p_tip, 3)
    
    #Tips
    pygame.draw.circle(screen, red, m_tip, 5)
    pygame.draw.circle(screen, green, p_tip, 5)
    
    pygame.display.update()
    sleep(2**-6)
    
pygame.display.quit()
