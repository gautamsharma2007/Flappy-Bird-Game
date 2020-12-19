import sys
import random
import pygame
from pygame.locals import *


FPS = 32
SCREENWIDTH=281
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUND={}
PLAYER='GALLERY FOR GAME/PICTURES FOR GAME/player.png'
BACKGROUND='GALLERY FOR GAME/PICTURES FOR GAME/background.png'
PIPE='GALLERY FOR GAME/PICTURES FOR GAME/pipe.png'



pygame.init()
FPSCLOCK=pygame.time.Clock()
pygame.display.set_caption('Flappy Bird by Gautam Sharma')
GAME_SPRITES['numbers']=(
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/0.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/1.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/2.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/3.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/4.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/5.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/6.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/7.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/8.png').convert_alpha(),
    pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/9.png').convert_alpha(),
)
GAME_SPRITES['message']=pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/message.png').convert_alpha()
GAME_SPRITES['base']=pygame.image.load('GALLERY FOR GAME/PICTURES FOR GAME/base.png').convert_alpha()
GAME_SPRITES['pipe']=(
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
)
GAME_SOUND['swoosh']=pygame.mixer.Sound('GALLERY FOR GAME/swoosh.wav')
GAME_SOUND['point']=pygame.mixer.Sound('GALLERY FOR GAME/point.wav')
GAME_SOUND['wing']=pygame.mixer.Sound('GALLERY FOR GAME/wing.wav')
GAME_SOUND['hit']=pygame.mixer.Sound('GALLERY FOR GAME/hit.wav')
GAME_SOUND['die']=pygame.mixer.Sound('GALLERY FOR GAME/die.wav')
GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
def welcomescreen():
    playery=int(SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2
    playerx=(SCREENWIDTH/20)
    messagex=int(SCREENWIDTH-GAME_SPRITES['message'].get_width())/2
    messagey=(SCREENHEIGHT*0)
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and event.key==K_SPACE:
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def getrandompipe():
    pipeheight=GAME_SPRITES['pipe'][0].get_height()
    offset=int(SCREENHEIGHT)/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    #y2=offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset)
    pipex=SCREENWIDTH+10
    y1=(pipeheight-y2)+offset
    pipe=[
        {'x':pipex,'y':-y1},
        {'x':pipex,'y':y2}    
    ]
    return pipe
def isCollide(playerx,playery,upperpipes,lowerpipes):
    if  playery>GROUNDY-25 or playery<=0:
        GAME_SOUND['hit'].play()
        return True 
    for pipe in upperpipes:
        pipeheight=GAME_SPRITES['pipe'][0].get_height()
        if playery<pipe['y']+pipeheight and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUND['hit'].play()
            return True 
    for pipe in lowerpipes:
         playerheight=GAME_SPRITES['player'].get_height()
         if (playery+playerheight>pipe['y']) and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width():
             GAME_SOUND['hit'].play()
             return True

    return False
def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT/2)
    basex=0
    pipe1=getrandompipe()
    pipe2=getrandompipe()
    upperpipes=[
        {'x':SCREENWIDTH+200,'y':pipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':pipe2[0]['y']}
    ]
    lowerpipes=[
        {'x':SCREENWIDTH+200,'y':pipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':pipe2[1]['y']}
    ]
    pipevelx=-4
    playervely=-9
    playermaxvely=10
    playerminy=-8
    playeracc=1
    playerflapvel=-8
    flap=False
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and event.key==K_SPACE:
                playervely=playerflapvel
                flap=True
                GAME_SOUND['wing'].play()
        crashtest=isCollide(playerx,playery,upperpipes,lowerpipes)
        if crashtest :
            return
        playermid=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipemid=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipemid<=playermid<pipemid+4:
                score+=1
                print("your score is",score)
                GAME_SOUND['point'].play() 
        if playervely<playermaxvely and not flap:
            playervely+=playeracc
        if flap:
            flap=False
        playerheight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playervely,GROUNDY-playery-playerheight)
        for lowerpipe,upperpipe in zip(lowerpipes,upperpipes):
            upperpipe['x']+=pipevelx
            lowerpipe['x']+=pipevelx
        if 0<upperpipes[0]['x']<5:
            newpipe=getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        for lowerpipe,upperpipe in zip(lowerpipes,upperpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        score=str(score)
        mydigits =[]
        for digit in score:
            
            mydigits.append(int(digit)) 

        width=0
        for digit in mydigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
        xoffset=(SCREENWIDTH-width)/2
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,SCREENHEIGHT*0.12))
            xoffset+=int(GAME_SPRITES['numbers'][digit].get_width())
        score=int(score)  
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
while True:
    welcomescreen()
    maingame()
    
