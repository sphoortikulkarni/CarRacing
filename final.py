from __future__ import print_function
import os
import sys
import pygame as pg
import time
import random
from pygame.locals import *
from textbox import TextBox
import pygame 
import fileinput
import cv2
from collections import deque
import numpy as np
import argparse
import math



pygame.init()
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 10
PLAYERMOVERATE = 8
COINMINSIZE = 10
COINMAXSIZE = 40
COINMINSPEED = 8
COINMAXSPEED = 8
ADDNEWCOINRATE = 20
ADDROADBLOCKRATE = 50
count=3
display_width = 800
display_height = 600 
black = (0,0,0)
white = (255,255,255) 
block_color = (53,115,255) 
car_width = 73 
red = (200,0,0)
green = (0,200,0)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
bright_red = (255,0,0)
bright_green = (0,255,0)
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Road Runner')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30) 
KEY_REPEAT_SETTING = (200,70)
font = pg.font.SysFont(None, 15)

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    time.sleep(2)
 
    game_loop()
    
    

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)


        
        
def game_intro1():

    intro = True
    app=Control()
    app1=Control1()
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(black)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Road Runner", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Register",150,450,100,50,green,bright_green,app1.main_loop)
        button("Login",550,450,100,50,green,bright_green,app.main_loop)
        pygame.display.update()
        clock.tick(15)
        
def waitForPlayerToPressKey0():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_loop()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    game_loop()
                return
                
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
def gamecontrol(moveLeft, moveRight, moveUp, moveDown):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 10)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720) 
    #cap.set(cv2.CAP_PROP_EXPOSURE , 0.1)
    cap.set(cv2.CAP_PROP_GAIN , 0.5)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    
    
    #cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    frame = cv2.medianBlur(frame,3)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_green = (29, 86, 6)
    upper_green = (64, 255, 255)
    thresh = cv2.inRange(hsv,lower_green, upper_green)
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    #print(best_cnt, max_area)
    M = cv2.moments(best_cnt)
    divfactor = max_area/10000.0
    if(divfactor < 1):
        divfactor = 1
    if(M['m00']>0 and max_area>100):
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(frame,(cx,cy),5,255,-1)
        #print(cx,cy)
        if(cx>198):
            moveRight = False
            moveLeft = True
            print('Left movement captured !')
        else:
            moveLeft = False
            moveRight = True
            print('Right movement captured !')
        if(cy>108):
            moveUp = False
            moveDown = True
        else:
            moveDown = False
            moveUp = True
    else:
        print("invisible")
        #pyautogui.click()
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    res = (255-res)
    res=cv2.flip(res,1)
    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    return moveLeft, moveRight, moveUp, moveDown


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    terminate()
                return
                
def waitForPlayerToPressKey1():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_loop1()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    game_loop1()
                return

def waitForPlayerToPressKey2():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_loop2()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    game_loop2()
                return
def waitForPlayerToPressKey5():
    app=Control()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                app.main_loop()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape login
                    app.main_loop()
                return

def waitForPlayerToPressKey4():
    app=Control1()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                app.main_loop()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape registering
                    app.main_loop()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False


def playercollectsCoin(playerRect, coins):
    for c in coins:
        if playerRect.colliderect(c['rect']):
                coins.remove(c)
                return True
    return False

def playerHitsBlock(playerRect, blocks):	
    for d in blocks:
        blockcount=0
        if playerRect.colliderect(d['rect']): 
                blockcount+=1	
                return True
    return False
    
def playerHitsBlock1(playerRect, blocks,blockcount):	
    for d in blocks:
        if playerRect.colliderect(d['rect']):
            if blockcount<2:
                blockcount=blockcount+1
			    #print "hit"
			    #return blockcount
            else:
	            return 2
    return blockcount




def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(True)

# fonts
font = pygame.font.SysFont(None, 30)

# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/car.wav')
laugh = pygame.mixer.Sound('music/laugh.wav')


# images
playerImage = pygame.image.load('image/new1.png')
car4 = pygame.image.load('image/car3.png')
coinsimg = pygame.image.load('image/bc.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample = [car4,baddieImage]
sample2 = [coinsimg]
wallRight = pygame.image.load('image/right.png')
wallLeft = pygame.image.load('image/left3.png')
roadblock = pygame.image.load('image/rb.png')
sample3 = [roadblock]

playerImage2 = pygame.image.load('image/new1.png')
car42 = pygame.image.load('image/car3.png')
police = pygame.image.load('image/police.png')
coinsimg = pygame.image.load('image/bc.png')
playerRect2 = playerImage2.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample22 = [car4,baddieImage,police]
sample2 = [coinsimg]
wallRight2 = pygame.image.load('image/right2.png')
wallLeft2 = pygame.image.load('image/left.png')
#roadblock = pygame.image.load('image/rock.png')
fire = pygame.image.load('image/fire.png')
sample32 = [fire]

#playerImage = pygame.image.load('image/new1.png')
#car4 = pygame.image.load('image/car3.png')
#coinsimg = pygame.image.load('image/bc.png')
#playerRect = playerImage.get_rect()
#baddieImage = pygame.image.load('image/car2.png')
#sample = [car4,baddieImage]
#sample2 = [coinsimg]
wallRight3 = pygame.image.load('image/right4.jpg')
wallLeft3 = pygame.image.load('image/left4.png')
roadblock = pygame.image.load('image/rb.png')
sample3 = [roadblock]


def quitgame():
	terminate()

def game_loop():
	pos=0
	cNo=0
	# "Start" screen
	#drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
	pygame.display.update()
	#waitForPlayerToPressKey()
	zero=0
	count=2
	if not os.path.exists("data/save.txt"):
		f=open("data/save.txt",'a')
		#f.write(str(zero))
		f.close()   
	v=open("data/save.txt",'r')
	topScore = int(v.readline())
	v.close()

	if not os.path.exists("data/coins.txt"):
		f2=open("data/coins.txt",'a')
		#f2.write(str(zero))
		f2.close()   
	v2=open("data/coins.txt",'r')
	topCoins = int(v2.readline())
	v2.close()


	while (count>0):
		
		# start of the game
		baddies = []
		coins= []
		blocks=[]
		score = 0
		blockcount = 0
		playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
		moveLeft = moveRight = moveUp = moveDown = False
		reverseCheat = slowCheat = False
		baddieAddCounter = 0
		coinAddCounter = 0
		blockAddCounter = 0 #add roadblocks- level 2
		pygame.mixer.music.play(-1, 0.0)

		while score!=100: # the game loop
		    score += 1 # increase score
		    moveLeft, moveRight, moveUp, moveDown = gamecontrol(moveLeft, moveRight, moveUp, moveDown)
		    
		    if score==100:
		        gameDisplay.fill(black)
		        drawText('Level 1 Completed!', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
		        drawText('You have unlocked level 2. Press Esc To play level 2', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
		        pygame.display.update()
		        waitForPlayerToPressKey1()
                
		    for event in pygame.event.get():
		        
		        if event.type == QUIT:
		            terminate()
		    '''
		        if event.type == KEYDOWN:
		            if event.key == ord('z'):
		                reverseCheat = True
		            if event.key == ord('x'):
		                slowCheat = True
		            if event.key == K_LEFT or event.key == ord('a'):
		                moveRight = False
		                moveLeft = True
		            if event.key == K_RIGHT or event.key == ord('d'):
		                moveLeft = False
		                moveRight = True
		            if event.key == K_UP or event.key == ord('w'):
		                moveDown = False
		                moveUp = True
		            if event.key == K_DOWN or event.key == ord('s'):
		                moveUp = False
		                moveDown = True

		        if event.type == KEYUP:
		            if event.key == ord('z'):
		                reverseCheat = False
		                score = 0
		            if event.key == ord('x'):
		                slowCheat = False
		                score = 0
		            if event.key == K_ESCAPE:
		                    terminate()
		        

		            if event.key == K_LEFT or event.key == ord('a'):
		                moveLeft = False
		            if event.key == K_RIGHT or event.key == ord('d'):
		                moveRight = False
		            if event.key == K_UP or event.key == ord('w'):
		                moveUp = False
		            if event.key == K_DOWN or event.key == ord('s'):
		                moveDown = False
			'''
		        

		    # Add new baddies at the top of the screen
		    if not reverseCheat and not slowCheat:
		        baddieAddCounter += 1
		    if baddieAddCounter == ADDNEWBADDIERATE:
		        baddieAddCounter = 0
		        baddieSize =30 
		        newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 28, 47),
		                    'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
		                    'surface':pygame.transform.scale(random.choice(sample), (28, 47)),
		                    }
		        baddies.append(newBaddie)
		        sideLeft= {'rect': pygame.Rect(0,0,126,600),
		                   'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
		                   'surface':pygame.transform.scale(wallLeft, (126, 599)),
		                   }
		        baddies.append(sideLeft)
		        sideRight= {'rect': pygame.Rect(497,0,303,600),
		                   'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
		                   'surface':pygame.transform.scale(wallRight, (303, 599)),
		                   }
		        baddies.append(sideRight)


		 # Add new coins
		    if not reverseCheat and not slowCheat:
		        coinAddCounter += 1
		    if coinAddCounter == ADDNEWCOINRATE:
		        coinAddCounter = 0
		        coinSize = 35 
		        newCoin = {'rect': pygame.Rect(random.randint(140, 485), 0 - coinSize, 28, 47),
		                    'speed': random.randint(COINMINSPEED, COINMAXSPEED),
		                    'surface':pygame.transform.scale(random.choice(sample2), (28, 47)),
		                    }
		        coins.append(newCoin)



		#add roadblocks
		    if not reverseCheat and not slowCheat:
		        blockAddCounter += 1
		    if blockAddCounter == ADDROADBLOCKRATE:
		        blockAddCounter = 0
		        blockSize =50 
		        newBlock = {'rect': pygame.Rect(random.randint(140, 485), 0 - blockSize, 23, 47),
		                    'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
		                    'surface':pygame.transform.scale(random.choice(sample3), (60, 35)),
		                    }
		        blocks.append(newBlock)
	
		      
		                    
	
		    # Move the player around.
		    if moveLeft and playerRect.left > 0:
		        playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
			#print("moved left")
			#pos-=1
			#print(pos)
		#playerRect.Find("playerImage").transform.position
		    if moveRight and playerRect.right < WINDOWWIDTH:
		        playerRect.move_ip(PLAYERMOVERATE, 0)
			#print("moved right")
			#pos+=1
			#print(pos)
		    if moveUp and playerRect.top > 0:
		        playerRect.move_ip(0, -1 * PLAYERMOVERATE)
		    if moveDown and playerRect.bottom < WINDOWHEIGHT:
		        playerRect.move_ip(0, PLAYERMOVERATE)
		    
		    for b in baddies:
		        if not reverseCheat and not slowCheat:
		            b['rect'].move_ip(0, b['speed'])
		        elif reverseCheat:
		            b['rect'].move_ip(0, -5)
		        elif slowCheat:
		            b['rect'].move_ip(0, 1)

		     
		    for b in baddies[:]:
		        if b['rect'].top > WINDOWHEIGHT:
		            baddies.remove(b)



		    for c in coins:
		        if not reverseCheat and not slowCheat:
		            c['rect'].move_ip(0, c['speed'])
		        elif reverseCheat:
		            c['rect'].move_ip(0, -5)
		        elif slowCheat:
		            c['rect'].move_ip(0, 1)

		     
		    

		#for blocks
		    for d in blocks:
		        if not reverseCheat and not slowCheat:
		            d['rect'].move_ip(0, d['speed'])
		        elif reverseCheat:
		            d['rect'].move_ip(0, -5)
		        elif slowCheat:
		            d['rect'].move_ip(0, 1)

		     
		    for d in blocks[:]:
		        if d['rect'].top > WINDOWHEIGHT:
		            blocks.remove(d)


		    # Draw the game world on the window.
		    windowSurface.fill(BACKGROUNDCOLOR)

		    # Draw the score and top score.
		    drawText('Score: %s' % (score), font, windowSurface, 128, 0)
		    drawText('coins: %s' % (cNo), font, windowSurface, 128, 20)
		    drawText('Top Score: %s' % (topScore), font, windowSurface,128, 40)
		    drawText('Rest Life: %s' % (count), font, windowSurface,128, 60)
		    
	
		    windowSurface.blit(playerImage, playerRect)
		    final=open("data/save1.txt",'w')
		    final.write(str(score))
		    
		    for b in baddies:
		        windowSurface.blit(b['surface'], b['rect'])


		    for c in coins:
		        windowSurface.blit(c['surface'], c['rect'])


		    for d in blocks:
		        windowSurface.blit(d['surface'], d['rect'])
	

		    pygame.display.update()

		    # Check if any of the car have hit the player.
		    if playerHasHitBaddie(playerRect, baddies):
		        g=open("data/save.txt",'a')
		        g.write(str(score))
		        g.write("\n")
		        #g.close()
		        gc=open("data/coins.txt",'a')	
		        gc.write(str(cNo))
		        gc.write("\n")
		        gc.close()	
		        if score > topScore:
		            topScore = score
		        break
                

		# Check if any of the car have hit the player.
		    if playercollectsCoin(playerRect, coins):
		        cNo=cNo+1		
		        if cNo>topCoins:
		            topCoins=cNo
	   	    #break	

		#if player hits block
		    if playerHitsBlock(playerRect, blocks):
		        blockcount+=1
		        if blockcount>=2:
		            count=count-1
		        break
		        with fileinput.FileInput("data/login.dat", inplace=True, backup='.bak') as file:
		            for line in file:
		                print(line.replace(score1, score), end='')

	

		    mainClock.tick(FPS)
		    



		# "Game Over" screen.
		pygame.mixer.music.stop()
		count=count-1
		cNo=0
	    
		gameOverSound.play()
		time.sleep(1)
		if (count==0):
		 laugh.play()
		 drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
		 drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
		 pygame.display.update()
		 time.sleep(2)
		 waitForPlayerToPressKey()
		 count=3
		 gameOverSound.stop()
	j=open("data/player.dat",'r')
	score1=str(j.readline())
	score=str(score)
	with fileinput.FileInput("data/login.dat", inplace=True, backup='.bak') as file:
	    for line in file:
	        print(line.replace(score1, score), end='')
		
def game_loop1():
    # "Start" screen
    #drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
    pygame.display.update()
    #waitForPlayerToPressKey()
    zero=0
    cNo=0
    count=3
    if not os.path.exists("data/save.txt"):
        f=open("data/save.txt",'a')
        #f.write(str(zero))
        f.close()   
    v=open("data/save.txt",'r')
    topScore = (v.readline())
    v.close()

    if not os.path.exists("data/coins.txt"):
        f2=open("data/coins.txt",'a')
        #f2.write(str(zero))
        f2.close()   
    v2=open("data/coins.txt",'r')
    topCoins = int(v2.readline())
    v2.close()


    while True:
        # start of the game
        baddies = []
        coins= []
        blocks=[]
        score = 0
        blockcount = 0
        playerRect2.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
        moveLeft = moveRight = moveUp = moveDown = False
        reverseCheat = slowCheat = False
        baddieAddCounter = 0
        coinAddCounter = 0
        blockAddCounter = 0 #add roadblocks- level 2
        pygame.mixer.music.play(-1, 0.0)

        while(score!=200): # the game loop
            score += 1 # increase score
            moveLeft, moveRight, moveUp, moveDown = gamecontrol(moveLeft, moveRight, moveUp, moveDown)

	
            if score==200:
                gameDisplay.fill(black)
                drawText('Level 2 Completed!', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                drawText('You have unlocked level3.Press Esc to go to level 3', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
                pygame.display.update()
                #time.sleep(2)
                waitForPlayerToPressKey2()

            for event in pygame.event.get():
                
                if event.type == QUIT:
                    terminate()
            '''

                if event.type == KEYDOWN:
                    if event.key == ord('z'):
                        reverseCheat = True
                    if event.key == ord('x'):
                        slowCheat = True
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveLeft = False
                        moveRight = True
                    if event.key == K_UP or event.key == ord('w'):
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveUp = False
                        moveDown = True

                if event.type == KEYUP:
                    if event.key == ord('z'):
                        reverseCheat = False
                        score = 0
                    if event.key == ord('x'):
                        slowCheat = False
                        score = 0
                    if event.key == K_ESCAPE:
                            terminate()
                

                    if event.key == K_LEFT or event.key == ord('a'):
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = False
                    if event.key == K_UP or event.key == ord('w'):
                        moveUp = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        moveDown = False

            '''            

            # Add new baddies at the top of the screen
            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieSize =30 
                newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 28, 47),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(random.choice(sample22), (28, 47)),
                            }
                baddies.append(newBaddie)
                sideLeft= {'rect': pygame.Rect(0,0,126,600),
                           'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                           'surface':pygame.transform.scale(wallLeft2, (126, 599)),
                           }
                baddies.append(sideLeft)
                sideRight= {'rect': pygame.Rect(497,0,303,600),
                           'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                           'surface':pygame.transform.scale(wallRight2, (303, 599)),
                           }
                baddies.append(sideRight)


	     # Add new coins
            if not reverseCheat and not slowCheat:
                coinAddCounter += 1
            if coinAddCounter == ADDNEWCOINRATE:
                coinAddCounter = 0
                coinSize = 35 
                newCoin = {'rect': pygame.Rect(random.randint(140, 485), 0 - coinSize, 23, 47),
                            'speed': random.randint(COINMINSPEED, COINMAXSPEED),
                            'surface':pygame.transform.scale(random.choice(sample2), (23, 47)),
                            }
                coins.append(newCoin)



	    #add roadblocks i.e. rock man in level2
            if not reverseCheat and not slowCheat:
                blockAddCounter += 1
            if blockAddCounter == ADDROADBLOCKRATE:
                blockAddCounter = 0
                blockSize =90 
                newBlock = {'rect': pygame.Rect(random.randint(190, 500), 0 - blockSize, 30, 50),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(random.choice(sample32), (40, 65)),
                            }
                blocks.append(newBlock)
	
              
                            
	
            # Move the player around.
            if moveLeft and playerRect2.left > 0:
                playerRect2.move_ip(-1 * PLAYERMOVERATE, 0)
	        #print("moved left")
	        #pos-=1
	        #print(pos)
	    #playerRect2.Find("playerImage2").transform.position
            if moveRight and playerRect2.right < WINDOWWIDTH:
                playerRect2.move_ip(PLAYERMOVERATE, 0)
	        #print("moved right")
	        #pos+=1
	        #print(pos)
            if moveUp and playerRect2.top > 0:
                playerRect2.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect2.bottom < WINDOWHEIGHT:
                playerRect2.move_ip(0, PLAYERMOVERATE)
            
            for b in baddies:
                if not reverseCheat and not slowCheat:
                    b['rect'].move_ip(0, b['speed'])
                elif reverseCheat:
                    b['rect'].move_ip(0, -5)
                elif slowCheat:
                    b['rect'].move_ip(0, 1)

             
            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    baddies.remove(b)



            for c in coins:
                if not reverseCheat and not slowCheat:
                    c['rect'].move_ip(0, c['speed'])
                elif reverseCheat:
                    c['rect'].move_ip(0, -5)
                elif slowCheat:
                    c['rect'].move_ip(0, 1)

             
            

	    #for blocks
            for d in blocks:
                if not reverseCheat and not slowCheat:
                    d['rect'].move_ip(0, d['speed'])
                elif reverseCheat:
                    d['rect'].move_ip(0, -5)
                elif slowCheat:
                    d['rect'].move_ip(0, 1)

             
            for d in blocks[:]:
                if d['rect'].top > WINDOWHEIGHT:
                    blocks.remove(d)


            # Draw the game world on the window.
            windowSurface.fill(BACKGROUNDCOLOR)

            # Draw the score and top score.
            drawText('Score: %s' % (score), font, windowSurface, 128, 0)
            drawText('coins: %s' % (cNo), font, windowSurface, 128, 20)
            drawText('Top Score: %s' % (topScore), font, windowSurface,128, 40)
            drawText('Rest Life: %s' % (count), font, windowSurface,128, 60)
            
	
            windowSurface.blit(playerImage2, playerRect2)
	
            
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])

            for c in coins:
                windowSurface.blit(c['surface'], c['rect'])

            for d in blocks:
                windowSurface.blit(d['surface'], d['rect'])
	

            pygame.display.update()

            # Check if any of the car have hit the player.
            if playerHasHitBaddie(playerRect2, baddies):
	            g=open("data/save.txt",'a')
	            g.write(str(score))
	            g.write("\n")
                #g.close()
	            gc=open("data/coins.txt",'a')	
	            gc.write(str(cNo))
	            gc.write("\n")
	            gc.close()
	            topScore=int(topScore)
	            if score > topScore:
	                topScore = score
	    # Check if any of the car have hit the player.
	            break

            if playercollectsCoin(playerRect2, coins):
	            cNo=cNo+1
	    #if player hits block
            if cNo>topCoins:		
                topCoins=cNo
       		#break	
        bcc=0
        bcc=playerHitsBlock1(playerRect2, blocks,bcc)
	    #print bcc
        bcc=bcc+1
        if bcc>=2:
            bcc=0
            break
            
            
            
            mainClock.tick(FPS)
	
		
		

            


        # "Game Over" screen.
        pygame.mixer.music.stop()
        count=count-1
        cNo=0
       
        gameOverSound.play()
        time.sleep(1)
        if (count==0):
         laugh.play()
         drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
         drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
         pygame.display.update()
         time.sleep(2)
         waitForPlayerToPressKey()
         count=3
         gameOverSound.stop()

def game_loop2():
    count=3
    cNo=0
    # "Start" screen
    #drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
    pygame.display.update()
    #waitForPlayerToPressKey()
    zero=0
    if not os.path.exists("data/save.txt"):
        f=open("data/save.txt",'a')
        #f.write(str(zero))
        f.close()   
    v=open("data/save.txt",'r')
    topScore = (v.readline())
    v.close()

    if not os.path.exists("data/coins.txt"):
        f2=open("data/coins.txt",'a')
        #f2.write(str(zero))
        f2.close()   
    v2=open("data/coins.txt",'r')
    topCoins = (v2.readline())
    v2.close()


    while (count>0):
        # start of the game
        baddies = []
        coins= []
        blocks=[]
        score = 0
        blockcount = 0
        playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
        moveLeft = moveRight = moveUp = moveDown = False
        reverseCheat = slowCheat = False
        baddieAddCounter = 0
        coinAddCounter = 0
        blockAddCounter = 0 #add roadblocks- level 2
        pygame.mixer.music.play(-1, 0.0)

        while (score!=300): # the game loop
            score += 1 # increase score
            moveLeft, moveRight, moveUp, moveDown = gamecontrol(moveLeft, moveRight, moveUp, moveDown)
            
            if score==300:
                drawText('You are a winner', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                #drawText('Press any key to next level.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
                pygame.display.update()
                time.sleep(2)
                waitForPlayerToPressKey()		


            for event in pygame.event.get():
                
                if event.type == QUIT:
                    terminate()
        
                
                        
            # Add new baddies at the top of the screen
            if not reverseCheat and not slowCheat:
                baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                baddieSize =30 
                newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(random.choice(sample), (23, 47)),
                            }
                baddies.append(newBaddie)
                sideLeft= {'rect': pygame.Rect(0,0,126,600),
                           'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                           'surface':pygame.transform.scale(wallLeft3, (126, 599)),
                           }
                baddies.append(sideLeft)
                sideRight= {'rect': pygame.Rect(497,0,303,600),
                           'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                           'surface':pygame.transform.scale(wallRight3, (303, 599)),
                           }
                baddies.append(sideRight)


	     # Add new coins
            if not reverseCheat and not slowCheat:
                coinAddCounter += 1
            if coinAddCounter == ADDNEWCOINRATE:
                coinAddCounter = 0
                coinSize = 35 
                newCoin = {'rect': pygame.Rect(random.randint(140, 485), 0 - coinSize, 28, 47),
                            'speed': random.randint(COINMINSPEED, COINMAXSPEED),
                            'surface':pygame.transform.scale(random.choice(sample2), (28, 47)),
                            }
                coins.append(newCoin)



	    #add roadblocks
            if not reverseCheat and not slowCheat:
                blockAddCounter += 1
            if blockAddCounter == ADDROADBLOCKRATE:
                blockAddCounter = 0
                blockSize =50 
                newBlock = {'rect': pygame.Rect(random.randint(140, 485), 0 - blockSize, 28, 47),
                            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                            'surface':pygame.transform.scale(random.choice(sample3), (60, 35)),
                            }
                blocks.append(newBlock)
	
              
                            
	
            # Move the player around.
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
	        #print("moved left")
	        #pos-=1
	        #print(pos)
	    #playerRect.Find("playerImage").transform.position
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(PLAYERMOVERATE, 0)
	        #print("moved right")
	        #pos+=1
	        #print(pos)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -1 * PLAYERMOVERATE)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, PLAYERMOVERATE)
            
            for b in baddies:
                if not reverseCheat and not slowCheat:
                    b['rect'].move_ip(0, b['speed'])
                elif reverseCheat:
                    b['rect'].move_ip(0, -5)
                elif slowCheat:
                    b['rect'].move_ip(0, 1)

             
            for b in baddies[:]:
                if b['rect'].top > WINDOWHEIGHT:
                    baddies.remove(b)


            for c in coins:
                if not reverseCheat and not slowCheat:
                    c['rect'].move_ip(0, c['speed'])
                elif reverseCheat:
                    c['rect'].move_ip(0, -5)
                elif slowCheat:
                    c['rect'].move_ip(0, 1)

             
            

	    #for blocks
            for d in blocks:
                if not reverseCheat and not slowCheat:
                    d['rect'].move_ip(0, d['speed'])
                elif reverseCheat:
                    d['rect'].move_ip(0, -5)
                elif slowCheat:
                    d['rect'].move_ip(0, 1)

             
            for d in blocks[:]:
                if d['rect'].top > WINDOWHEIGHT:
                    blocks.remove(d)


            # Draw the game world on the window.
            windowSurface.fill(BACKGROUNDCOLOR)

            # Draw the score and top score.
            drawText('Score: %s' % (score), font, windowSurface, 128, 0)
            drawText('coins: %s' % (cNo), font, windowSurface, 128, 20)
            drawText('Top Score: %s' % (topScore), font, windowSurface,128, 40)
            drawText('Rest Life: %s' % (count), font, windowSurface,128, 60)
            
	
            windowSurface.blit(playerImage, playerRect)
	
            
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])


            for c in coins:
                windowSurface.blit(c['surface'], c['rect'])


            for d in blocks:
                windowSurface.blit(d['surface'], d['rect'])
	

            pygame.display.update()

            # Check if any of the car have hit the player.
            if playerHasHitBaddie(playerRect, baddies):
                g=open("data/save.txt",'a')
                g.write(str(score))
                g.write("\n")
                #g.close()
                gc=open("data/coins.txt",'a')
                gc.write(str(cNo))
                gc.write("\n")
                gc.close()
                topScore=int(topScore)	
                if score > topScore:
                    topScore = score
                break

	    # Check if any of the car have hit the player.
            topCoins=int(topCoins)
            if playercollectsCoin(playerRect, coins):
	            cNo=cNo+1
	            
            if cNo>topCoins:
                topCoins=cNo
       		#break	

	    #if player hits block
        if playerHitsBlock(playerRect, blocks):
	            blockcount+=1
	            break
	            
	
            
            
            
                #mainClock.tick(FPS)



        # "Game Over" screen.
        pygame.mixer.music.stop()
        count=count-1
        cNo=0
       
        gameOverSound.play()
        time.sleep(1)
        if (count==0):
         laugh.play()
         drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
         drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
         pygame.display.update()
         time.sleep(2)
         waitForPlayerToPressKey()
         count=3
         gameOverSound.stop()


         Fwa
    
class Control(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption("Road Runner")
        self.screen = pg.display.set_mode((800,600))
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.input = TextBox((200,135,150,30),command=self.change_color,
                              clear_on_enter=True,inactive_on_enter=False)
	
        self.color = (0,0,0)
        self.prompt = self.make_prompt(20,10,100,'Please Login!')
        self.prompt1 = self.make_prompt(20,10,135,'Username')
        self.prompt2 = self.make_prompt(40,300,35,'Road Runner')
	

        pg.key.set_repeat(*KEY_REPEAT_SETTING)

    def make_prompt(self,font,size1,size2,text):
        font = pg.font.SysFont("arial", font)
        message = text
        rend = font.render(message, True, pg.Color("white"))
        return (rend, rend.get_rect(topleft=(size1,size2)))

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.input.get_event(event)
	    

    def change_color(self,id,color):
        #zero=0
        #try:
            #if not os.path.exists("data/save.dat"):
                #f=open("data/login.dat",'w')
                #f.write(str(zero))
                #f.close()
            #game_intro1()   
            f=open("data/login.dat",'r+')
            #topScore = f.readline()
            
	   
	    #f = open("file.txt", "r")

            #searchlines = f.readlines()
            #f.close()

            for columns in ( raw.strip().split() for raw in f ):
                if(columns[0]==str(color)):
                    global abcd
                    abcd=columns[1]
                    print (columns[0])
                    print(columns[1])
                    columns[1]=int(columns[1])
                    #f3=open("data/player.dat",'w')
                    #f3.write(columns[1])
                    print(columns[1])
                    intro = True

                    while intro:
                        for event in pygame.event.get():
                            #print(event)
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                                
                        gameDisplay.fill(black)
                        largeText = pygame.font.SysFont("comicsansms",115)
                        TextSurf, TextRect = text_objects("Road Runner", largeText)
			#TextSurf, TextRect = text_objects("Dodge enemy cars and collect coins to complete a level", largeText)
                        TextRect.center = ((display_width/2),(display_height/2))
                        gameDisplay.blit(TextSurf, TextRect)
                        #f=open("data/player.dat",'r+')
                        #for columns in ( raw.strip().split() for raw in f ):
                         #           columns[0]=int(columns[0])
                        
                        if(columns[1]<100 and columns[1]>=0):
                                        button("Level1",150,450,100,50,green,bright_green,game_loop)
                                        button("Quit",550,450,100,50,green,bright_green,quitgame)
                        elif(columns[1]<200 and columns[1]>100):
                                        button("Level1",150,450,100,50,green,bright_green,game_loop)
                                        button("Quit",550,450,100,50,green,bright_green,quitgame)
                                        button("level2",350,450,100,50,green,bright_green,game_loop1)
                                        #button("Level3",550,450,100,50,green,bright_green,cannot)
                        elif(columns[1]>200):
                                        button("Level1",150,450,100,50,green,bright_green,game_loop)
                                        button("Quit",350,550,100,50,green,bright_green,quitgame)
                                        button("level2",350,450,100,50,green,bright_green,game_loop1)
                                        button("Level3",550,450,100,50,green,bright_green,game_loop2)
                                        
                                        
                        
                        pygame.display.update()
                        clock.tick(15)
                #else:
                 #   drawText('Incorrect Username', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
                  #  pygame.display.update()
                   # waitForPlayerToPressKey5()
                    
			
           
	    
        #except ValueError:
        #    print("Please input a valid color name.")

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.input.update()
            self.screen.fill(self.color)
            self.input.draw(self.screen)
            self.screen.blit(*self.prompt)
            self.screen.blit(*self.prompt1)
            self.screen.blit(*self.prompt2)
            pg.display.update()
            self.clock.tick(self.fps)
            
#Class for register            
class Control1(object):
    def __init__(self):
        pg.init()
        pg.display.set_caption("Road Runner")
        self.screen = pg.display.set_mode((800,600))
        self.clock = pg.time.Clock()
        self.fps = 80.0
        self.done = False
        self.input = TextBox((200,135,150,30),command=self.change_color,
                              clear_on_enter=True,inactive_on_enter=False)
	
        self.color = (0,0,0)
        self.prompt = self.make_prompt(20,10,100,'Enter A Number For Registration Which Will Be Used During Your Login')
        self.prompt1 = self.make_prompt(20,10,135,'Username')
        self.prompt2 = self.make_prompt(40,300,35,'Road Runner')
	

        pg.key.set_repeat(*KEY_REPEAT_SETTING)

    def make_prompt(self,font,size1,size2,text):
        font = pg.font.SysFont("arial", font)
        message = text
        rend = font.render(message, True, pg.Color("white"))
        return (rend, rend.get_rect(topleft=(size1,size2)))

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.input.get_event(event)
	    

    def change_color(self,id,color):
        zero=0
        app=Control()
        try:
            f=open("data/login.dat", "r")
            #for i in range(2):
            for columns in ( raw.strip().split() for raw in f ):
                if(isinstance(int(color), int)):
                    if(columns[0]!=str(color)):
                        f=open("data/login.dat", "a")
                        f.write("%s %s\n" % (color,zero))
                        drawText('Register Successful.Please Press Esc key To start The Level 1', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
                        pygame.display.update()
                        waitForPlayerToPressKey0()
                    else:
                        drawText('Username Already Exists.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
			#drawText('\nPress ESC key to enter new username', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
                        pygame.display.update()
                        waitForPlayerToPressKey4()
                else:
                    drawText('Only Digits as Username', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
                    pygame.display.update()
                    waitForPlayerToPressKey4()
        except ValueError:
                drawText('Only Digits as Username', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
                pygame.display.update()
                waitForPlayerToPressKey4()


    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.input.update()
            self.screen.fill(self.color)
            self.input.draw(self.screen)
            self.screen.blit(*self.prompt)
            self.screen.blit(*self.prompt1)
            self.screen.blit(*self.prompt2)
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    app = Control()
    game_intro1()
    #app.main_loop()
    pg.quit()
    sys.exit()
