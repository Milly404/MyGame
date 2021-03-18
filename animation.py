import pygame, sys

player_run = []
player_run.append(pygame.image.load('img\WuKong 1.png'))
player_run.append(pygame.image.load('img\WuKong 2.png'))
player_run.append(pygame.image.load('img\WuKong 3.png'))
player_run.append(pygame.image.load('img\WuKong 4.png'))

class Player(pygame.sprite.Sprite):
  def __init__(self, pos_x, pos_y):
     super().__init__()
     self.run_animation = False
     self.sprites = player_run

     self.current_sprite = 0
     self.image = self.sprites[self.current_sprite]
     self.rect = self.image.get_rect()
     self.rect.topleft = [pos_x,pos_y]


  def update(self,speed):
     self.current_sprite += speed
     if int(self.current_sprite) >= len(self.sprites):
        self.current_sprite = 0
        self.run_animation = False
     self.image = self.sprites[int(self.current_sprite)]

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player(100,100)
moving_sprites.add(player)

while True:
  for event in pygame.event.get():
     if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


  # Drawing
  screen.fill((0,0,0))
  moving_sprites.draw(screen)
  moving_sprites.update(0.25)
  pygame.display.flip()
  clock.tick(60)
