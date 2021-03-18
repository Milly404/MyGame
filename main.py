# Milly & Fiona
# FM207
# Mar 4 2021

import pygame
import random
import os
from random import random, randint, seed
import controller

p1 = controller.Controller(0)

pygame.init()
vInfo = pygame.display.Info()
#size = WIDTH, HEIGHT = vInfo.current_w, vInfo.current_h #适合大小
size = WIDTH, HEIGHT = 1200,900 #固定大小
FPS=1
VEL=10
BLACK = 0,0,0

#images 照片
#find the folder of images 找到我们可爱的照片文件夹
game_folder=os.path.dirname(__file__)
img_folder=os.path.join(game_folder,"img")

#background 背景照片导入
background=pygame.image.load(os.path.join(img_folder,"background right.png"))
background_rect=background.get_rect()

#icon 图标导入
icon = pygame.image.load(os.path.join(img_folder,"icon.png"))
pygame.display.set_icon(icon)

#obstacle 障碍导入
stone=pygame.image.load(os.path.join(img_folder,"Stone.png"))
stone_rect=stone.get_rect()

#player 人物照片导入
# WuKong1=pygame.image.load(os.path.join(img_folder,"WuKong 1.png"))
# WuKong1_rect=WuKong1.get_rect()
# Wukong=WUkong_x,Wukong_y=139,602   #7,602

#run images
player_run = [
    os.path.join(img_folder, "WuKong 1.png"),
    os.path.join(img_folder, "WuKong 2.png"),
    os.path.join(img_folder, "WuKong 3.png"),
    os.path.join(img_folder, "WuKong 4.png"),
]

#jump images
player_jump = [
    os.path.join(img_folder,"WuKong 6.png"),
    os.path.join(img_folder,"WuKong 5.png"),
    os.path.join(img_folder,"WuKong 6.png"),
]

#initialize pygame and create window 创造窗口
pygame.init()
#screen=pygame.display.set_mode(size, pygame.RESIZABLE) #可移动的屏幕有机会再说
#screen=pygame.display.set_mode(size, pygame.NOFRAME)#无边框
#screen=pygame.display.set_mode(size, pygame.FULLSCREEN) #诶嘿搞个全屏就快乐了
screen=pygame.display.set_mode(size)
pygame.display.set_caption("FM207") #give the game a name 给它个名字

#setup player
class Player(pygame.sprite.Sprite):
   #sprite for the player

   def __init__(self):
       pygame.sprite.Sprite.__init__(self)
       self.image=pygame.image.load(os.path.join(img_folder,"WuKong 1.png"))
       self.rect=self.image.get_rect()
       self.rect.center=139,602
       self.y_speed=1
       self.rect.bottom=830
       self.level=2
       self.levelChange=10
       self.joystick_pressed = False

       # self.images=player_run
       # self.image=self.images['run'][0]
       #
       # self.rect=self.image.get_rect()
       # self.mask=pygame.mask.from_surface(self.image)
       # self.rect.left, self.rect.top=position
       # self.rect.top-=1
       #
       # self.state='run'
       # self.is_up=False
       # self.init.speed=10*FPS/1000
       # self.base_height=BASE_HEIGHT

   def update(self):
       self.y_speed=0
       keys=pygame.key.get_pressed()
       y1 = 530
       y2 = 675
       y3 = 830

       if self.joystick_pressed == False:
           self.level += p1.get_y_axis()

       if p1.get_y_axis() != 0:
           self.joystick_pressed = True
       else:
           self.joystick_pressed = False

       if p1.is_button_just_pressed("a"):
           self.level += 1
       elif p1.is_button_just_pressed("b"):
           self.level -= 1

       if self.level > 3:
           self.level = 3
       elif self.level < 1:
           self.level = 1

       if self.level == 1:
           self.rect.bottom = y1
       elif self.level == 2:
           self.rect.bottom = y2
       else:
           self.rect.bottom = y3


       # if event.type==pygame.KEYDOWN:
       #     if event.key==pygame.K_UP:
       #         if self.rect.bottom==y2 or y1:
       #             self.rect.bottom=y1
       #         if self.rect.bottom==y3:
       #             self.rect.bottom=y2
       #     elif event.key==pygame.K_DOWN:
       #         if self.rect.bottom==y2 or y3:
       #             self.rect.bottom=y3
       #         if self.rect.bottom==y1:
       #             self.rect.bottom=y2
       #     elif event.type==pygame.KEYUP:
       #         player_movey=1
       # elif event.type==pygame.KEYUP:
       #     if event.key==pygame.K_UP:
       #          if self.rect.bottom == y2:
       #              self.rect.bottom = y2
       #          if self.rect.bottom == y3:
       #              self.rect.bottom = y3
       #          if self.rect.bottom==y1:
       #              self.rect.bottom=y1
       #     elif event.key==pygame.K_DOWN:
       #         if self.rect.bottom == y2:
       #             self.rect.bottom = y2
       #         if self.rect.bottom == y3:
       #             self.rect.bottom = y3
       #         if self.rect.bottom == y1:
       #             self.rect.bottom = y1


all_sprites=pygame.sprite.Group() #group all of them
player=Player()
all_sprites.add(player) #add player1

#run game 开始冲冲冲
while True:

    p1.update()

    for event in pygame.event.get():
        #close the window
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE: #close the window with Esc
                sys.exit()

        # 测试xy轴
        #elif event.type == pygame.MOUSEMOTION:#鼠标所在位置
            #print("[MOUSEMOTION]:", event.pos,event.rel, event.buttons)
        #elif event.type == pygame.MOUSEBUTTONUP:#鼠标释放
            #print("[MOUSEBUTTONUP]:", event.pos, event.button)
        elif event.type == pygame.MOUSEBUTTONDOWN:#鼠标点击
            print("[MOUSEBUTTONDOWN]:", event.pos, event.button)

        # 可移动并保持移动的窗口
        #elif event.type == pygame.VIDEORESIZE:
            #size = WIDTH,HEIGHT = event.size[0],event.size[1]
            #screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    #draw /render打印背景
    screen.blit(background,background_rect)

    #打印人物
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.update()
pygame.quit()