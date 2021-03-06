# Milly & Fiona
# FM207
# Mar 4 2021

import pygame, sys, time
import random
import os
from random import random, randint, seed
import controller
from time import sleep

p1 = controller.Controller(0)

pygame.init()
vInfo = pygame.display.Info()
#size = WIDTH, HEIGHT = vInfo.current_w, vInfo.current_h #适合大小
size = WIDTH, HEIGHT = 1200,900 #固定大小
FPS=30
VEL = 10
y = 675
y1 = 530
y2 = 675
y3 = 830
vel_y = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

#images 照片
#find the folder of images 找到我们可爱的照片文件夹
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")

menu = pygame.image.load(os.path.join(img_folder,"menu.png"))
menu_rect = menu.get_rect()

#background 背景照片导入
bg1 = pygame.image.load(os.path.join(img_folder,"background left.png"))
bg2 = pygame.image.load(os.path.join(img_folder,"background left.png"))

x1 = 0
x2 = -1200

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

player_run = []
player_run.append(pygame.image.load('img\WuKong 1.png'))
player_run.append(pygame.image.load('img\WuKong 2.png'))
player_run.append(pygame.image.load('img\WuKong 3.png'))
player_run.append(pygame.image.load('img\WuKong 4.png'))
player_run.reverse()

#jump images
player_jump = []
player_jump.append(pygame.image.load('img\WuKong 6.png'))
player_jump.append(pygame.image.load('img\WuKong 5.png'))
player_jump.append(pygame.image.load('img\WuKong 6.png'))

#obstacle images
obstacle_img = []
obstacle_img.append(pygame.image.load('img\Stone.PNG'))
obstacle_img.append(pygame.image.load('img\HuLu.PNG'))
#obstacle_img.append(pygame.image.load('img\JingJiaoDaWang.PNG'))
#obstacle_img.append(pygame.image.load('img\PanTao.PNG'))

#initialize pygame and create window 创造窗口
pygame.init()
clock = pygame.time.Clock()
#screen=pygame.display.set_mode(size, pygame.RESIZABLE) #可移动的屏幕有机会再说
#screen=pygame.display.set_mode(size, pygame.NOFRAME)#无边框
#screen=pygame.display.set_mode(size, pygame.FULLSCREEN) #诶嘿搞个全屏就快乐了
screen=pygame.display.set_mode(size)
pygame.display.set_caption("FM207") #give the game a name 给它个名字

font = pygame.font.SysFont('Arial', 45)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# 抽象出一个方法用来绘制Text在屏幕上
def showText(fontObj, text, x, y):
    textSurfaceObj = fontObj.render(text, True, GREEN, WHITE)  # 配置要显示的文字
    textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
    textRectObj.center = (x, y)  # 设置显示对象的坐标
    screen.blit(textSurfaceObj, textRectObj)  # 绘制字体

fontbigObj = pygame.font.SysFont('Arial', 30)  # 通过字体文件获得字体对象
fontminObj = pygame.font.SysFont('Arial', 20)  # 通过字体文件获得字体对象

def show_go_screen():
    screen.blit(menu, menu_rect)
    draw_text('Press  (A)  to  start', font, (45, 95, 204), screen, 420, 658)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def Game_over():
    screen.fill(BLACK)
    draw_text('GAME OVER', font, (225,225,225), screen, 450, 400)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def bg_move():

    global x1,x2

    x1 -= 4
    x2 -= 4

    screen.blit(bg1, (x1,0))
    screen.blit(bg2, (x2, 0))

    if x1 < -1200:
        x1 = 1200
    if x2 < -1200:
        x2 = 1200

    return x1, x2

#setup player
class Player(pygame.sprite.Sprite):
   #sprite for the player

   def __init__(self):
       pygame.sprite.Sprite.__init__(self)

       super().__init__()
       #self.run_animation = False
       self.animation_speed = 8
       self.animation_counter = 0
       self.frame_ratio = int(FPS/self.animation_speed)
       self.sprites = player_run
       self.current_sprite = 0
       self.image = self.sprites[self.current_sprite]
       self.rect = self.image.get_rect()

       self.radius = int(self.rect.width / 3)
       #self.mask = pygame.mask.from_surface(self.image)
       pygame.draw.circle(self.image,GREEN,self.rect.center,self.radius)
       
       self.sprites_jump=player_jump
       self.current_sprite_jump = 1
       self.image = self.sprites_jump[self.current_sprite_jump]
       self.rect = self.image.get_rect()
       self.allow_jump=False

       self.rect.center = 139, 602
       self.y_speed = 1
       self.rect.bottom = 830
       self.level = 2
       self.levelChange = 10
       self.joystick_pressed = False

   def run_animation(self,speed):

       global FPS

       self.animation_counter += 1

       if self.animation_counter == self.frame_ratio:
           self.animation_counter = 0
           self.current_sprite += speed

       if int(self.current_sprite) >= len(self.sprites):
           self.current_sprite = 0
       self.image = self.sprites[int(self.current_sprite)]

   def jump(self,speed):

       global FPS

       self.animation_counter += 1

       if self.animation_counter == self.frame_ratio:
           self.animation_counter = 0
           self.current_sprite_jump += speed

       if int(self.current_sprite_jump) >= len(self.sprites_jump):
           self.current_sprite_jump = 0
       self.image = self.sprites_jump[int(self.current_sprite_jump)]

   def update(self):

       global vel_y

       jump = False

       self.run_animation(1)

       self.y_speed=0


       if self.joystick_pressed == False and jump is False:
           self.level += p1.get_y_axis()

       if p1.get_y_axis() != 0:
           self.joystick_pressed = True
       else:
           self.joystick_pressed = False

       # if p1.is_button_just_pressed("a"):
       #     self.level += 1
       # elif p1.is_button_just_pressed("b"):
       #     self.level -= 1

       if self.level > 3:
           self.level = 3
       elif self.level < 1:
           self.level = 1

       if self.level == 1:
           self.rect.bottom = y1
           y = self.rect.bottom
       elif self.level == 2:
           self.rect.bottom = y2
           y = self.rect.bottom
       else:
           self.rect.bottom = y3

       if jump is False and p1.is_button_just_pressed("a"):
           jump = True

       if jump is True:
           #y -= vel_y
           #vel_y -= 1
           #if vel_y < -10:
               #jump = False
               #vel_y = 10
       #if p1.is_button_just_pressed("a"):

           self.rect.top = self.rect.top - 150
           #self.player_sj = pygame.time.get_ticks()
           #print (self.player_sj)
           self.jump(1)

       pygame.time.delay(100)



       #if self.allow_jump==True and pygame.time.get_ticks()-self.player_sj<=1300:
            #self.rect.top = self.rect.top + 100
            #self.allow_jump=False


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


class obstacle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = obstacle_img
        self.current_sprite = randint(0,1)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 3)
        pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        #yuan lai shi 560
        y1 = randint(0,2)*150+540
        self.rect.bottomleft = (randint(970,1000000),y1)
        self.start_time=pygame.time.get_ticks()


    def update(self):
        if self.start_time and pygame.time.get_ticks()-self.start_time > 2000:
            self.start_time=False
        self.rect.x-=5

# 初始化计时器
counts = 0
# 自定义计时事件
COUNT = pygame.USEREVENT + 1
# 每隔1秒发送一次自定义事件
pygame.time.set_timer(COUNT, 1000)

game_over = True
running = True
#run game 开始冲冲冲
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()  # group all of them
        obstacles = pygame.sprite.Group()
        for Obstacle in range(1, 10000):
            Obstacle = obstacle()
            all_sprites.add(Obstacle)  # add obstacle
            obstacles.add(Obstacle)
        player = Player()
        all_sprites.add(player)  # add player1

    clock.tick(FPS)

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
    x1, x2 = bg_move()

    #打印人物
    all_sprites.update()



    #check to see if hit
    hits = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_circle)
    #if circle_x < rect_x + circle_width and circle_x + rect_width > rect_x:
    if hits:
        Game_over()
        #sleep(3)
        game_over = True

    all_sprites.draw(screen)
    for event in pygame.event.get():  # 获取事件
        if event.type == COUNT:  # 判断事件是否为计时事件
            counts = counts + 1
            countstext = str(counts)
            showText(fontbigObj, countstext, 600, 50)

    pygame.display.update()
pygame.quit()
