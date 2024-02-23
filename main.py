'''importing and initializing pygame'''

import pygame
import random
import math

from pygame import mixer

# initialize the pygame 
pygame.init()


'''creating the screen'''

# create the screen
screen=pygame.display.set_mode((800,600))


'''adding background'''

# background
background=pygame.image.load('background.png')



'''changing the title,logo'''

# Title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)



'''Adding background music and sound effects'''
mixer.music.load('background.mp3')
mixer.music.play(-1)

'''Adding images into our space invader game'''

#player
playerImg=pygame.image.load('player.png')
playerX=370
playerY=480
playerX_change=0

def player(x,y):
    screen.blit(playerImg,(x,y))


'''creating multiple enemies'''

enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

'''creating an enemy'''

#enemy
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))


'''creating bullets for shooting'''


#bullet

# ready-you can't see the bullet on the screen
# fire-the bullet is currently moving

bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))


'''collision detection'''

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False

'''Adding text and displaying score'''

# score
# score=0
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

def show_score(x,y):
    score=font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))


# game over text
over_font=pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    game_over=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over,(200,250))



'''game loop'''

# game loop
running=True
while running:

    '''change background color'''
    screen.fill((0,0,0))

    # background image
    screen.blit(background,(0,0))

    # playerY-=0.1


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        '''keyboard input controls and keyboard press events'''
        
        # check if keystroke is pressed and check whether its right or left
        if event.type==pygame.KEYDOWN:
            # print("A key is pressed")
            if event.key==pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change=-5
            if event.key==pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        
        if event.type==pygame.KEYUP:
            # print("A key is released")
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                # print("Left or right keystroke has been released") 
                playerX_change=0

    playerX+=playerX_change

    '''Adding boundaries to the game'''



    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    


    '''movement mechanics of enemy space invaders'''


    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[i]=2000
            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]

        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        

        # collision
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1
            # print(score)
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)
        

        enemy(enemyX[i],enemyY[i],i)
    

    # bullet Movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"


    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    

    


    show_score(textX,textY)
    player(playerX,playerY)

    pygame.display.update()


