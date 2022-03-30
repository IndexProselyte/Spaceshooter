# Import of all required modules/libraries
import os
import random
import time
import pygame as pg
from pygame.locals import *
from datetime import datetime

#######################################################
# Constants
#######################################################

# Screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Zmení názov programu
SCREEN_CAPTION = "Game"
SCREEN_FPS = 20

# Zmení iconu programu
SCREEN_ICON = "iranian_children.png.jpg"

# Pozadie hry
SCREEN_BGIMAGE = "screen_background.png"
COLOR_BLANK = pg.Color("black")

# MISC 
PLAY_ALERT = True
TTD = 300
VICTORY = False

# File System
# Do constanty ulozime cestu k images folderu
# Tím ze spojíme assets a images dokopy
DIR_ASSETS_IMAGES = os.path.join("assets", "images")
DIR_ASSETS_SOUNDS = os.path.join("assets", "sounds")
DIR_ASSETS_MUSIC = os.path.join("assets", "music")

#print(DIR_ASSETS_IMAGES)

# Assets File Names aby sme ich mohli lahko meniť
FILE_IMG_Player = "player.png"
FILE_IMG_Enemy = "Asteroid Brown.png"
FILE_IMG_Bullet = "missile.png"
FILE_IMG_Bullet_SP = "player.png"
FILE_MUS_Background = "hra1 main_track.ogg"
FILE_SFX_Fire = "fire.wav"
FILE_SFX_SP_Fire = "space laser.wav"
FILE_SFX_PlayerExplosion = "player_explosion.wav"
FILE_SFX_EnemyExplosion = "enemy_explosion.wav"
FILE_SFX_Alert = "alert.wav"
FILE_SFX_Meteor_Alert = "meteor_alert.wav"

# Game
GAME_ENEMY_COUNT = 10
CURRENT_ENEMY_COUNT = 0

#######################################################
# Utility
#######################################################

# loads music file from assets folder
def LoadMusic(fileName):
    pg.mixer.music.load(os.path.join(DIR_ASSETS_MUSIC, fileName))

# loads image file from assets folder
def LoadImage(fileName): 
    # Toto nám vráti cestu: assets/images/filename
    return pg.image.load(os.path.join(DIR_ASSETS_IMAGES, fileName))

# loads sound file from assets folder
def LoadSound(fileName):
    return pg.mixer.Sound(os.path.join(DIR_ASSETS_SOUNDS, fileName))

#  TODO : Understand and fix
# draw a given text of given size to given surface on given position
def DrawText(surface, text, fontess, size, x, y):
    # Setneme font
    font_name = pg.font.match_font(fontess)
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, pg.Color('white'))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# quits to system
def QuitGame():
    pg.quit()
    exit(0)


#######################################################
# PyGame Initialization
#######################################################
pg.init()
# module for fonts
pg.font.init()
# module for loading and playing sounds & music
pg.mixer.init()

pg.display.set_icon(LoadImage(SCREEN_ICON))
pg.display.set_caption(SCREEN_CAPTION)
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()


#######################################################
# Load assets
#######################################################

# load images pomocou Loadimage funkcie 
# Toto nám uloží cestu od assets po daný súbor ktorý máme ako parameter
IMG_background = LoadImage(SCREEN_BGIMAGE)
IMG_player = LoadImage(FILE_IMG_Player)
IMG_enemy = LoadImage(FILE_IMG_Enemy)
IMG_bullet = LoadImage(FILE_IMG_Bullet)
IMG_bullet_SP = LoadImage(FILE_IMG_Bullet_SP)

# load music
LoadMusic(FILE_MUS_Background)

# load sounds
SFX_SP_Fire = LoadSound(FILE_SFX_SP_Fire)
SFX_Fire = LoadSound(FILE_SFX_Fire)
SFX_PlayerExplosion = LoadSound(FILE_SFX_PlayerExplosion)
SFX_EnemyExplosion = LoadSound(FILE_SFX_EnemyExplosion)
SFX_Alert = LoadSound(FILE_SFX_Alert)
SFX_METEOR_ALERT = LoadSound(FILE_SFX_Meteor_Alert)
#######################################################
# Define sprites
#######################################################

class Player(pg.sprite.Sprite):
    # default variables
    __PLAYER_Width__ = 50
    __PLAYER_Height__ = 30
    __PLAYER_SpeedX__ = 5
    __PLAYER_Speedy__ = 5

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        # Tunak si upravíme výšku a šírku obrázku Playera aby nám nezaberal viac miesta ako treba
        # Parametre v tejto funkcií sú (Súbor ktorý upravujeme, (úprava x súradnice, úprava y súradnice))
        self.image = pg.transform.scale(IMG_player, (Player.__PLAYER_Width__, Player.__PLAYER_Height__))
        
        # Tunak získame bounding box 
        self.rect = self.image.get_rect()
        
        # Zacinajuca pozícia playera
        # x je v strede a y je 50px od zeme
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 50
        
        # Tuto zadávame rýchlost pohybu po x a y suradniciach
        self.speedx = 0
        self.speedy = 0
        
        # Checkujeme pohyb a meníme ho pomocou Constant
    def goLeft(self, proceed = False):
        if proceed:
            self.speedx -= Player.__PLAYER_SpeedX__
        else:
            self.speedx = 0

    def goRight(self, proceed = False):
        if proceed:
            self.speedx += Player.__PLAYER_SpeedX__
        else:
            self.speedx = 0
    
    def goUp(self, proceed = False):
        if proceed:
            self.speedy -= Player.__PLAYER_Speedy__
        else:
            self.speedy = 0
    
    def goDown(self, proceed = False):
        if proceed:
            self.speedy += Player.__PLAYER_Speedy__
        else:
            self.speedy = 0
    
        # Vytvorenie bullet projectilu ktory ma x a y parametre v argumentoch
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        # Pridanie do skupiny spritov
        all_sprites.add(bullet)
        bullets.add(bullet)
    
    def shoot_SP(self):
        sp_bullet = SP_Bullet(self.rect.centerx, self.rect.top)
        # Pridanie do skupiny spritov
        all_sprites.add(sp_bullet)
        sp_bullets.add(sp_bullet)
    
    def update(self):
        # Makes you move
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # don't let the sprite goes over the left and right screen borders BORDERS
        # self.rect.right ti vrati x koordinacie pravej strany obdlznika
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.top < 0:
            self.rect.top = SCREEN_HEIGHT - 599
        
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Creates the enemy class
class Enemy(pg.sprite.Sprite):
    # Premmena na zrýchlovanie meteoritov po každom zostrelení
    badVar = 0

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        # Vybere si náhodnu velkost
        self.sizex = random.randrange(10, 100)
        # Zobere x velkost a vynasobí ju aby meteority lepsie vyzerali
        self.sizey = random.randrange(int(self.sizex * 0.8), int(self.sizex * 1.2))
        
        # Zmení velkost enemy spritu pomocou náhodných parametrou
        self.image = pg.transform.scale(IMG_enemy, (self.sizex, self.sizey))
        
        # Znova získame bounding box
        self.rect = self.image.get_rect()

        # Získame náhodnu x,y suradnicu 
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        # Získame náhodnú rýchlost pre pohyb dolu a do šikma
        self.speedx = random.randrange(-5, 8)
        self.speedy = random.randrange(3, 12) + Enemy.badVar

    def update(self):
        # Vloz rýchlost do suradnic
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Ak sa dostane meteorit pod playera a cez okno tak ho vrat na nahodnu suradnicu hore
        # A daj mu nahodnu rychlost
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

        # AK sa dotkne steni tak sa odraz 
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speedx *= -1
        
       # Ak toto odkomentujem tak sa budu odrazat od zeme
       # if self.rect.up < 0 or self.rect.down > SCREEN_HEIGHT:
           # self.speedy *= 1

class Bullet(pg.sprite.Sprite):
    # defaults
    __BULLET_SpeedY__ = 10

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # do image ulozime string s nazvom bullet spritu
        self.image = IMG_bullet
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        # y suradnica sa bude zmensovat podla bullet_speedY co znamena ze pojde hore
        self.rect.y -= Bullet.__BULLET_SpeedY__

        # delete current Sprite and remove it from all Sprite Groups ak sa dotkne zeme
        if self.rect.bottom < 0:
            self.kill()

class SP_Bullet(pg.sprite.Sprite):
    # defaults
    __BULLET_SpeedY__ = 20

    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # do image ulozime string s nazvom bullet spritu
        self.image = IMG_bullet_SP
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        # y suradnica sa bude zmensovat podla bullet_speedY co znamena ze pojde hore
        self.rect.y -= Bullet.__BULLET_SpeedY__

        # delete current Sprite and remove it from all Sprite Groups ak sa dotkne zeme
        if self.rect.bottom < 0:
            self.kill()

#######################################################
# Game functions
#######################################################
# Ak držím klavesu tak nech sa pohnem
def HandleKeyDownEvent(KeyDownEvent):
    if KeyDownEvent.key == pg.K_a:
        player.goLeft(True)
    if KeyDownEvent.key == pg.K_d:
        player.goRight(True) 
    if KeyDownEvent.key == pg.K_w:
        player.goUp(True)
    if KeyDownEvent.key == pg.K_s:
        player.goDown(True)
 
# Shoot function
    if KeyDownEvent.key == pg.K_SPACE:
        player.shoot()

# Ale ak som pustil klavesu tak nech sa nehybem
def HandleKeyUpEvent(KeyUpEvent):
    if KeyUpEvent.key == pg.K_a:
        player.goLeft(False)
    if KeyUpEvent.key == pg.K_d:
        player.goRight(False)

    if KeyUpEvent.key == pg.K_w:
        player.goUp(False)
    if KeyUpEvent.key == pg.K_s:
        player.goDown(False) 

def writeScore(score):
    # Get the time and datew
    scorePath = "assets\stats\score.txt"
    current_DateTime = datetime.now()
    # Create a long string with the time and date
    Log = (
        "\n"
        f'This was your score: {score}\n'
        f"You achieved this in {current_DateTime}\n" 
         "Congratas Amogo :)\n"
        )
    # Write it to a txt file so you will have a list of scores
    # You will have to use "a" instead of the ususal write 
    # As "a" appends the text into the end of the file without deleting the previous contents
    with open(scorePath, 'a') as f:
            f.write(Log)

def victoryState():
    # Had to use a global here beacuze no other way worked and im lazy :)
    global TTD
    global CURRENT_ENEMY_COUNT
    global VICTORY
    # Check if the player has beaten the meteor storm
    if Enemy.badVar > 7:
        # Stops the spawning of meteors
        VICTORY = True
        DrawText(screen, "Congratulations You Have Won!","arial", 45, SCREEN_WIDTH /2, 30)

    else:
        if Enemy.badVar >= 2 and Enemy.badVar < 6.8:
            DrawText(screen, "Meteorite cluster incoming!!!","arial", 24, SCREEN_WIDTH /2, 35) 
            # Play scary effect 
            # OR NOT HUH????,
            # Start a countdown in the top right which will tell the player how long they need to survive
            DrawText(screen, str(TTD),"arial", 24, (SCREEN_WIDTH /2) + 250, 30)
        
            # Just not to overflow the fukcing counter-ass bitchlmao xddddddddddddddddddddddddddddddddddddddddddddd
            if TTD -1 < 0:
                TTD = 0
            else:    
                TTD -= 1

#######################################################
# Main + Overall Event Loop
#######################################################
# configujeme mixer a audio
pg.mixer.music.set_volume(0.1)
# Aby hralo nekonecno
pg.mixer.music.play(loops=-1)

# sprite groups to easy update all sprites
all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()
bullets = pg.sprite.Group()
sp_bullets = pg.sprite.Group()

# creation of Player sprite
player = Player()
all_sprites.add(player)

# creation of Enemy sprites and the enemies themselfs
for e in range(GAME_ENEMY_COUNT):
    CURRENT_ENEMY_COUNT += 1
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Stores player's score
score = 0
# Stores players special attack
sp_attack_counter = 5

running = True
while running:

    # loop through all events
    for event in pg.event.get():
        # print all events in console for debug purposes
        #print(event)

        # check for closing window event
        if event.type == pg.QUIT:
            writeScore(score)
            running = False
            QuitGame()
        
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.shoot()
            if event.button == 3:
                if sp_attack_counter > 13:
                    player.shoot_SP()
                    SFX_SP_Fire.play()
                    sp_attack_counter = 0
        
        # handle KeyDown event
        elif event.type == pg.KEYDOWN:
            HandleKeyDownEvent(event)
        # handle KeyUp event
        elif event.type == pg.KEYUP:
            HandleKeyUpEvent(event)
    
    # Check if the special is ready
    if sp_attack_counter > 13:
        if PLAY_ALERT:
            PLAY_ALERT = False
            SFX_Alert.play()

    # Resets the ability to play so it wont play continousli
    if sp_attack_counter < 13:
        PLAY_ALERT = True

    # update all sprites
    all_sprites.update()

    # check for collisions/hits among Bullet and Enemy sprites
    hits = pg.sprite.groupcollide(enemies, bullets, True, True)
    # check for collisions among(us) SP_bullets and enemies
    sp_hits = pg.sprite.groupcollide(enemies, sp_bullets, True, False)

    # add new enemies after some are killed + some other  stuff
    for hit in hits:
        CURRENT_ENEMY_COUNT -= 1
        sp_attack_counter += 1
        # Získane score sa zmensuje podla velkosti meteoritu
        score += 120 - hit.sizex
        #print(score)
        
        # Make the level harder the longer you play by first increasing the speed andd other things
        Enemy.badVar += 0.1

        # Here just to stop enemies from spawning after victory
        if VICTORY == False:
            # And then entering a meteorit megacluster.
            if TTD == 0:
                for i in range(2):
                    CURRENT_ENEMY_COUNT += 2    
                    newEnemy = Enemy()
                    all_sprites.add(newEnemy)
                    enemies.add(newEnemy)
                    
            CURRENT_ENEMY_COUNT += 1
            newEnemy = Enemy()
            all_sprites.add(newEnemy)
            enemies.add(newEnemy)

        # add new enemies after some are killed by the special attack
        for hit in sp_hits:
            score += 80 - hit.sizex
            #print(score)
            newEnemy = Enemy()
            all_sprites.add(newEnemy)
            enemies.add(newEnemy)

    # check for collisions between Player and Enemy sprites
    collisions = pg.sprite.spritecollide(player, enemies, True) # rectangle collision strategy
    if collisions:
        writeScore(score)
        SFX_PlayerExplosion.play()
        time.sleep(1)
        running = False

    # clear screen to blank color OR blit a background image before drawing a sceen again
    screen.blit(IMG_background, IMG_background.get_rect())

    # draw / render the sceen
    all_sprites.draw(screen)
    DrawText(screen, str(score),"arial", 18, SCREEN_WIDTH /2, 10)

    # Check if WE WERE VICTORIOUS HE HE HE HA!!!
    victoryState()

    # *after* drawing everything, flip/update the screen with what we've drawn
    pg.display.flip()
    #pg.display.update()

    # control the draw update speed
    clock.tick(SCREEN_FPS)
#######################################################
# Quit
#######################################################
QuitGame()
