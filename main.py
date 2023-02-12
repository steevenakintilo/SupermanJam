#!/usr/bin/env python3
##
## EPITECH PROJECT, 2021
## sd
## File description:
## d
##


import pygame
import random
from random import randint
import pygame.freetype 

SCREEN_HEIGHT = 1920
SCREEN_WIDTH = 1080

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

class DrawSprite(pygame.sprite.Sprite):
    def __init__(self,path):
        super(DrawSprite, self).__init__()
        self.surf = pygame.image.load(path).convert_alpha()
        self.rect = self.surf.get_rect()

class Window():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("music/main.ogg")
    pygame.mixer.music.play(-1)
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    state = 0

class Target():
    target_y = randint(0,1080 - 351)

class Player():
    sprite_height = 273
    sprite_width = 108
    x = 0
    y = 300
    hp = 0
    hp_draw = 0
    score = 0

class Laser():
    laser_x_list = []
    laser_y_list = []
    laser_pos_list = []
    laser_move = False

class Enemy():
    enemy_x_list = []
    enemy_y_list = []
    enemy_pos_list = []
    enemy_move = False
    enemy_nbr = 0
    enemy_speed = 0

def write_into_file(path,x):  
    f = open(path, "w")
    f.write(str(x))    
    f.close            

def print_file_content(path):
    f = open(path, 'r')
    content = f.read()
    return(content)
    f.close()

def move_player(p):
    pressed_key = pygame.key.get_pressed()
    if pressed_key[ord('z')] == True and p.y > 0:
        p.y -= 3
    if pressed_key[ord('s')] == True and p.y < 1055 - p.sprite_width:
        p.y += 3
    
def create_laser(p,l):
    l.laser_move = True
    if len(l.laser_pos_list) < 1:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/laser.ogg'))
        l.laser_y_list.append(p.y)
        l.laser_x_list.append(p.x)
        l.laser_pos_list.append(0)
    
def move_laser(l):
    if l.laser_move == True:
        for i in range(len(l.laser_pos_list)):
            l.laser_pos_list[i] += random.uniform(0.01, 10)
    
def delete_laser(l,p):
    try:
        for i in range(len(l.laser_pos_list)):
            if l.laser_pos_list[i] + l.laser_x_list[i] > 1920:
                l.laser_pos_list.remove(l.laser_pos_list[i])
                l.laser_x_list.remove(l.laser_x_list[i])
                l.laser_y_list.remove(l.laser_y_list[i])
    except:
        pass

def create_enemy(e,nbr):
    r = []
    rr = []
    for i in range(10):
        r.append(i * 65) if i != 0 else False
    for i in range(2):
        rr.append(1800 + (i * 65)) if i != 0 else False
        #rr.append(1800) if i != 0 else False
    if len(e.enemy_pos_list) < nbr:
        for i in range(len(rr)):
            e.enemy_pos_list.append(0)
            e.enemy_x_list.append(rr[randint(0,len(rr) - 1)])
            e.enemy_y_list.append(r[randint(0,len(r) - 1)])

def move_enemy(e):
    for i in range(len(e.enemy_pos_list)):
        e.enemy_pos_list[i] -= (1 + e.enemy_speed)

def check_colision_laser_enemy(l,e):
    for i in range(len(e.enemy_x_list)):
        for j in range(len(l.laser_pos_list)):
            #print(int(e.enemy_x_list[i]  + e.enemy_pos_list[i]) , int(l.laser_x_list[j] + l.laser_pos_list[j]))
            if e.enemy_x_list[i]  + e.enemy_pos_list[i] == l.laser_x_list[j] + l.laser_pos_list[j]:
                print("ok")
            #print(e.enemy_x_list[i],l.laser_x_list[j])
            #if l.laser_x_list[j] == e.enemy_x_list[i]:

def delete_enemy(e):
    try:
        for i in range(len(e.enemy_pos_list)):
            if e.enemy_x_list[i] + e.enemy_pos_list[i] < -65:
                e.enemy_x_list[i] = 1800 + (i * 65)
                if i < 10:
                    e.enemy_y_list[i] = (i * 65)
                else:
                    e.enemy_y_list[i] = (randint(2,10) * 65)
                e.enemy_pos_list[i] = 0
    except:
        pass

def check_colision_player_enemy(p,e):
    for i in range(len(e.enemy_x_list)):
        if e.enemy_x_list[i]  + e.enemy_pos_list[i] <= 108 and e.enemy_x_list[i]  + e.enemy_pos_list[i] >= 43 and p.y <= e.enemy_y_list[i] + 54 and p.y >= e.enemy_y_list[i] - 54:
            p.hp -= 0.1 + (p.score/100)
            p.hp_draw += 19.20 * (0.1 + p.score/100)

def check_colision_target(l,t,p,e):
    for j in range(len(l.laser_pos_list)):
        #print(1920 - 374,1920,int(l.laser_x_list[j] + l.laser_pos_list[j]+187),int(l.laser_x_list[j] + l.laser_pos_list[j]-187))
        if (1920 - 374) <= int(l.laser_x_list[j] + l.laser_pos_list[j] + 187) and t.target_y - 187 <= int(l.laser_y_list[j] - 54 - 187) and t.target_y + 187 <= int(l.laser_y_list[j] + 54 + 187):     
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/hit.ogg'))
            l.laser_pos_list.remove(l.laser_pos_list[j])
            l.laser_x_list.remove(l.laser_x_list[j])
            l.laser_y_list.remove(l.laser_y_list[j])
            t.target_y = randint(0,1080 - 351)
            p.score += 1
            e.enemy_speed += 0.1
            #quit()

def main_game(w):
    white = (255,255,255)
    w = Window()
    red = (255,0,0)
    player = DrawSprite("pic/superman.png")
    laser = DrawSprite("pic/laser.jpg")
    enemy = DrawSprite("pic/rock.png")
    target = DrawSprite("pic/target.png")
    bat = DrawSprite("pic/bat.png")
    p = Player()
    l = Laser()
    e = Enemy()
    t = Target()
    GAME_FONT = pygame.freetype.Font("font/font.ttf", 75)
    running = True
    file_score = int(print_file_content("highscore.txt"))
    end_game = False
    menu = True
    rect_1 = pygame.Rect(600, 380, 600, 82)
    rect_2 = pygame.Rect(600, 580, 600, 82)

    while running:
        for event in pygame.event.get():
            pressed_key = pygame.key.get_pressed()
            if pressed_key[ord('h')] == True:
                menu = False
            if pressed_key[ord('x')] == True:
                running = False
            if pressed_key[ord(' ')] == True:
                create_laser(p,l)
        
        w.screen.fill(white)
        pygame.draw.rect(w.screen, (255, 0, 0), rect_1,10)
        pygame.draw.rect(w.screen, (255, 0, 0), rect_2,10)
        GAME_FONT.render_to(w.screen, (730, 100), "SUPERJAM",(255,0,0))
        GAME_FONT.render_to(w.screen, (700, 400), "PRESS H TO START",(0,0,0))
        GAME_FONT.render_to(w.screen, (700, 600), "PRESS X TO QUIT",(0,0,0))
    
        if end_game == False and menu == False:
            move_player(p)
            create_enemy(e,p.score + 1)
            move_enemy(e)
            delete_enemy(e)
            move_laser(l)
            delete_laser(l,p)
            check_colision_player_enemy(p,e)
            check_colision_target(l,t,p,e)
            #check_colision_laser_enemy(l,e)
            w.screen.fill(white)
            rect = pygame.Rect(0, 1060, 1920 - int(p.hp_draw), 20)
            pygame.draw.rect(w.screen, red, rect)
            w.screen.blit(player.surf,(p.x,p.y))
            if p.hp_draw > 1920:
                end_game = True
            
            for i in range(len(e.enemy_pos_list)):
                enemyx = e.enemy_x_list[i] + e.enemy_pos_list[i]
                enemyy = e.enemy_y_list[i]
                
                w.screen.blit(enemy.surf,(enemyx,enemyy))
            for i in range(len(l.laser_x_list)):
                laserx = p.x + p.sprite_height - 20 + l.laser_x_list[i] + l.laser_pos_list[i]
                lasery = l.laser_y_list[i] + 10
                #screen.blit(laser.surf,(p.x + p.sprite_height - 20 + p.laser_x_list[i] ,p.laser_y_list[i] + 10))
                w.screen.blit(laser.surf,(laserx,lasery))
            w.screen.blit(target.surf,(1920 - 374,t.target_y))
            GAME_FONT.render_to(w.screen, (0, 0), "SCORE " + str(p.score),(0,0,0))
            if p.score > file_score:
                write_into_file("highscore.txt",str(p.score))
                GAME_FONT.render_to(w.screen, (0, 80), "HIGHSCORE " + str(p.score),(0,0,0))
            else:
                GAME_FONT.render_to(w.screen, (0, 80), "HIGHSCORE " + str(file_score),(0,0,0))
        elif menu == False and end_game == True:
            w.screen.fill(white)
            GAME_FONT.render_to(w.screen, (0, 0), "SCORE " + str(p.score),(0,0,0))
            if p.score > file_score:
                GAME_FONT.render_to(w.screen, (0, 80), "HIGHSCORE " + str(p.score),(0,0,0))
            else:
                GAME_FONT.render_to(w.screen, (0, 80), "HIGHSCORE " + str(file_score),(0,0,0))
            w.screen.blit(bat.surf,(700,600))
            GAME_FONT.render_to(w.screen, (700, 500), "GAME OVER",(0,0,0))
        pygame.display.flip()

def end_game():
    w = Window()
    running = True
    while running:
        white = (255,255,255)
        w.screen.fill(white)
        GAME_FONT = pygame.freetype.Font("font/font.ttf", 75)
        GAME_FONT.render_to(w.screen, (700, 500), "GAME OVER",(0,0,0))

def handle_event():
    pressed_key = pygame.key.get_pressed()
    if pressed_key[ord('x')] == True:
        running = False
    if pressed_key[ord(' ')] == True:
        create_laser(p,l)

def handle_state(w):
    if w.state == 0:
        main_game(w)

def start_game():
    w = Window()
    running = True
    main_game(w)
    #white = (255,255,255)
    

if __name__ == "__main__":
    start_game()
